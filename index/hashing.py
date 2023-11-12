import hashlib
from index.textExtractor import TextExtractor

class Hashing:
    def __init__(self, te):
        self.__hashes_set = set()
        self.__hash = ""
        self.__textExtracted = te

    def __get_signature(self, text):
        try:
            return hashlib.sha256(text.encode()).hexdigest()
        except:
            return False
        
    def __get_set_of_hashes(self, pages):
        try:
            child_nodes = set()
            for page in pages:
                new_hash = self.__get_signature(page)
                child_nodes.add(new_hash)
            self.__hashes_set =  child_nodes
        except:
            return False
        
    def make_hash(self):
        try:
            buffer = ""
            pages_hashes = self.__get_set_of_hashes(self.__textExtracted.get_pages())
            if(False == pages_hashes):
                return False, "Erro encontrado ao gerar hashes de paginas de arquivo"
            for hash in self.__hashes_set:
                buffer += hash
            file_hash = self.__get_signature(buffer)
            if(file_hash == False):
                return False, "Erro encontrado ao gerar hash de arquivo"
            self.__hash = file_hash
            return True, "OK"
        except Exception:
            return False, "Erro: {}".format(Exception.with_traceback)
        
    def get_hash(self):
        return self.__hash;

    def get_full_text(self):
        return self.__textExtracted.get_text()
    