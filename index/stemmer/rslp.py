import nltk
nltk.download('rslp')
from nltk.stem import RSLPStemmer
from unidecode import unidecode
import json


class RSLP:
    def __init__(self):
        self.st = RSLPStemmer()
        self.stopwords = self.ler_stopwords()
    
    def ler_stopwords(self):
        stopwords = []
        with open('config/portugueseST.json', 'r') as arquivo:
    # Carrega o conteúdo JSON do arquivo
            data = json.load(arquivo)
            stopwords = data['stopwords']
           # print(stopwords)
        return stopwords

    def text_stemming(self, text):
        try:
            stemmed_text = ""
            for token in text.split(' '):
                token = unidecode(token).lower()
                try:
                    stem = ""
                    if token not in self.stopwords:
                        stem = self.st.stem(token)
                except:
                    stem = ""
                stemmed_text = stemmed_text + stem + " "

            return stemmed_text       
        except Exception as e:
            return e + " Em stemmer.rslp "
        