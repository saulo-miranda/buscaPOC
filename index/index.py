from django.db import models


class Index:
    def __init__(self):
        self.__token_amount = 0
        self.__inverted_index = []
        self.__collection_size = 0
        self.__documents_length = {}
        self.__corpus_len = 0
        self.__average_document_len = 0
    
    def build_index(self, hashing):
        tokens = hashing.get_full_text().split()
        file_id = hashing.get_hash()
        for i, t in enumerate(tokens):
            self.__add_token(t, file_id, i)
        self.__collection_size += 1
        self.__documents_length[file_id]=len(tokens)
        self.__corpus_len += len(tokens)
        self.__average_document_len = self.__corpus_len / self.__collection_size
        print(self.__average_document_len)

    def __add_token(self, token, name, pos):
        if token in self.__inverted_index:
            documents = self.__inverted_index[token]
            if name in documents:
                self.__inverted_index[token][name]["positions"].append(pos)
                self.__inverted_index[token][name]["freq"] += 1
            else:
                self.__inverted_index[token][name] = {"positions":[pos], "freq": 1}
                self.__inverted_index[token]['documents'] += 1
        else:
            self.__inverted_index[token] = {"documents": 1, name: {"positions":[pos], "freq": 1}}
    
    def print_index(self):
        for t, v in sorted(self.__inverted_index.items()):
            print(t)
            print(v)

    def print_documents_len(self):
        for t, v in (self.__documents_length.items()):
            print(t, v)
