import os
from pathlib import Path
from pypdf import PdfReader
import re, json
from django_project import settings
from documentos.models import Token
from index.stemmer.savoy import Savoy
import yake
from unidecode import unidecode

class TextExtractor:
    def __init__(self, path):
        self.__CONFIG_ACCENT_FIX = 'config/accent_fix.json'
        self.__CONFIG_PUNCTUATION = 'config/punctuation.json'
        self.__text = ""
        self.__pages = []
        self.__path =  settings.BASE_DIR.__str__() +  path
        self.__savoy = Savoy()
        self.__words = 0

    def extrair_tokens(self, documento_id):
        try:
            termos = self.extract()
            tokens = []
            for termo in termos:
                print(termo)
                token_existente = next((t for t in tokens if t.termo == termo), None)
                if token_existente:
                    token_existente.incrementar()
                else:
                    novo_token = Token(termo, documento_id)
                    tokens.append(novo_token)
            Token.objects.bulk_create(objs=tokens, batch_size=1000)
            return tokens
        except Exception as e:
            return e
        
    def extract(self):
        try:
            pages = self.__get_pages()
            text = ""
            self.__get_text_pages(pages)
            for p in self.__pages:
                text = text + p
            self.__text = text
            return self.__text.split(' ')
        except Exception as e:
            self.__text =  e + " Em textExtractor.get_full_text"  


    def get_full_text(self):
        try:
            pages = self.__get_pages()
            text = ""
            self.__get_text_pages(pages)
            for p in self.__pages:
                text = text + p
            self.__text = text.replace('\n', ' ')
            self.__text = self.__text.replace(' ´', '')
            self.__text = self.__text.replace(' ˆ', '')
            self.__text = self.__text.replace(' ´', '')
            self.__text = self.__text.replace(' ~', '')
        #    self.__stem_document_savoy()
            return self.__text
        except Exception as e:
            self.__text =  e + " Em textExtractor.get_full_text"    

    def __get_pages(self):
        try:
            print(self.__path)
            return PdfReader(self.__path).pages
        except Exception as e:
            return e 
        
    def __get_text_pages(self, pages):
        try:
            text_pages = []
            n_pages = len(pages)
            for i in range(n_pages):
                text = pages[i].extract_text()
                #filtered_text = self.__pre_process(pages[i].extract_text())
                #filtered_text = self.__accent_fix(filtered_text)
                text_pages.append(text)
            self.__pages = text_pages
        except Exception as e:
            self.__pages = [e + " Em textExtractor.get_text_pages "]

    def __pre_process(self, page):
        try:
            text = self.__remove_new_line(page)
            text = self.__to_lower_case(text)
        #    text = self.__accent_fix(text)
            text = self.__remove_punctuation(text)
            text = self.__remove_short_words(text)
            return text
        except Exception as e:
            return e + " Em textExtractor.pre_process"

    def __remove_new_line(self, page):
        try:
            text = page.replace("\n", "")
            return text
        except Exception as e:
            return [e + " Em textExtractor.remove_new_line "]
    
    def __to_lower_case(self, page):
        try:
            text = page.lower()
            return text
        except Exception as e:
            return e + " Em textExtractor.to_lower_case"
    def __accent_fix(self, text):
        try:
            f = open(self.__CONFIG_ACCENT_FIX)
            rep = json.load(f) 
            rep = dict((re.escape(k), v) for k, v in rep.items()) 
            pattern = re.compile("|".join(rep.keys()))
            text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
            return text
        except Exception as e:
            return e + " Em textExtractor.accent_fix"
        
    def __remove_punctuation(self, page):
        try:
            f = open(self.__CONFIG_PUNCTUATION)
            rep = json.load(f) 
            rep = dict((re.escape(k), v) for k, v in rep.items()) 
            pattern = re.compile("|".join(rep.keys()))
            text = pattern.sub(lambda m: rep[re.escape(m.group(0))], page)
            return text
        except Exception as e:
            return [e + " Em textExtractor.remove_new_line "]

    def __remove_short_words(self, page):
        try:
            text = page.split(" ")
            filtered = ""
            for word in text:
                if len(word) > 2:
                    filtered = filtered + " " + word
            return filtered
        except Exception as e:
            return e + " Em textExtractor.remove_short_words"

    def get_preintroduction(self, page):
        abstract_pattern = '.*?Introdu' 
        abstract_text = re.findall(abstract_pattern, page)
        abstract_text = self.accent_fix(abstract_text[0])
        return abstract_text
    
    def get_abstract(self, page):
        abstract_pattern = 'Resumo.*?Introdu' 
        abstract_text = re.findall(abstract_pattern, page)
        abstract_text = self.__accent_fix(abstract_text[0])
        return abstract_text
    
    def get_pages(self):
        return self.__pages
    
    def get_text(self):
        return self.__text
    
    def __stem_document_savoy(self):
        stemmed_text = ""
        for word in self.__text.split(" "):
            stemmed_text = stemmed_text + " " + self.__savoy.stemming(word) 
        self.__text = stemmed_text
    
    def extract_full_text(self):
        try:
            pages = self.__get_pages()
            text = ""
            self.__get_text_pages(pages)
            for p in self.__pages:
                text = text + p
            self.__text = text.replace('\n', ' ')
            self.__text = self.__text.replace(' ´', '')
            self.__text = self.__text.replace(' ˆ', '')
            self.__text = self.__text.replace(' ´', '')
            self.__text = self.__text.replace(' ~', '') 
            self.__text = self.__text.replace('´', '')
        #    self.__stem_document_savoy()
        except Exception as e:
            self.__text =  e + " Em textExtractor.get_full_text"   

    def extrair_keywords(self, n):
        self.extract_full_text()
        language = "pt"
        max_ngram_size = 3
        deduplication_threshold = 0.9
        deduplication_algo = 'seqm'
        windowSize = 1

        custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=n, features=None)
        keywords = custom_kw_extractor.extract_keywords(self.__text)
        palavras_unicas = []
        for k in keywords:
            print(k)
            termo = k[0]
            for w in termo.split(' '):
                palavras_unicas.append(unidecode(w).lower())
        conjunto = set(palavras_unicas)
        palavras_unicas = list(conjunto)
        print(palavras_unicas)

        return palavras_unicas

    def get_quantidade_de_palavras(self):
        if self.__words == 0:
            self.__words = len(self.__text.split(' '))
        return self.__words