import os, glob, json, re, hashlib
from index.stemmer.savoy import Savoy
from index.textExtractor import TextExtractor
from index.index import Index
from index.hashing import Hashing
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')

class Ingest:

    def __init__(self):
        self.__CONFIG_REPO_PATH =  os.path.dirname(os.path.realpath(__file__)) +  '/config/repo_path.json'
        self.__CONFIG_ACCENT_FIX =  os.path.dirname(os.path.realpath(__file__)) +  '/config/accent_fix.json'
        self.__CONFIG_PUNCTUATION =  os.path.dirname(os.path.realpath(__file__)) +  '/config/punctuation.json'
        self.__repo_dir = 'media' #self.__read_repo_path_from_json()
        self.__document_files = []
        self.__index = Index()
        self.__savoy = Savoy()
        self.stopwords = stopwords.words('portuguese')

    def process_file(self, filename):
        try:
            path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', self.__repo_dir, filename))
            text_extractor = TextExtractor(path)
            text_extractor.extract()
            text = text_extractor.get_text()
            text = self.__pre_process(text)
            text = self.__stem_document_savoy(text)
            hash_value = hashlib.sha256(text.encode()).hexdigest()
            return hash_value, path, text
        except Exception as e:
            print("ERRO:  " + e)

    def process_file_test(self, text, doc_id):
        try:
            filtered_text = self.__pre_process(text)
            filtered_text = self.__stem_document_savoy(filtered_text)
            hash_value = hashlib.sha256(filtered_text.encode()).hexdigest()
            return hash_value, doc_id, text
        except Exception as e:
            print("ERRO:  " + e)

    def read_pdf_files(self):
        try:
            pdf_files = []
            for arquivo in glob.glob(os.path.join(self.__repo_dir, '*.pdf')):
                pdf_files.append(arquivo)
            self.__document_files = pdf_files
        except Exception as e:
            print("ERRO:  " + e)

    def __read_repo_path_from_json(self):
        f = open(self.__CONFIG_REPO_PATH)
        data = json.load(f)
        return data["path"]
    
    def insert_files(self):
        try:
            
            for f in self.__get_documents_names():
                text_extractor = TextExtractor(f )
                text_extractor.get_full_text()
                hashing = Hashing(f, text_extractor)
                hashing.make_hash()
                self.__index.insert_document(hashing)
        except Exception as e:
            print("ERRO:  " + e)

    def insert_files_test(self, text, doc_id):
        try:
            filtered_text = self.__pre_process(text)
            hashing = Hashing(doc_id, filtered_text)
            hashing.make_hash_test()
            self.__index.insert_document(hashing)
        except Exception as e:
            print("ERRO:  " + e)

    def __get_documents_names(self):
        return self.__document_files
    
    def print_index(self):
        self.__index.print_index()

    def print_doc_len(self):
        self.__index.print_documents_len()
    
    def get_index(self):
        return self.__index
    

    def __pre_process(self, page):
        try:
            text = self.__remove_new_line(page)
            text = self.__to_lower_case(text)
            text = self.__accent_fix(text)
            text = self.__remove_punctuation(text)
            text = self.__remove_stopwords(text)
         #   text = self.__remove_short_words(text)
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

    def __stem_document_savoy(self, text):
        stemmed_text = ""
        for word in text.split(" "):
            stemmed_text = stemmed_text + " " + self.__savoy.stemming(word) 
        return stemmed_text
    
    def __remove_stopwords(self, page):
        page_terms = page.split(" ")
        filtered = [term for term in page_terms if term not in self.stopwords]
        text = ' '.join(filtered)
        return text