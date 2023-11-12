import unicodedata

class Savoy:
    def __init__(self):
        pass

    def text_stemming(self, text):
        text = text.split()
        stemmed_text = ""
        for word in text:
            stemmed_text = stemmed_text + self.stemming(word) + " "
        return stemmed_text

    def stemming(self, word):
         
        word = self.remove_suffix(word)
         
        word = self.norm_feminin(word)
         
        word = self.final_vowel(word)
         
        word = self.remove_accent(word)
        return word

    def remove_accent(self, word):
        encoded = unicodedata.normalize("NFD", word)
        encoded = encoded.encode("ascii", "ignore")
        encoded = encoded.decode("utf-8")
        return encoded
    
    def final_vowel(self, word):
        length = len(word)-1
        if(length > 3 and (word[length] in {"a", "e", "o"})):
            return word[:length]
        return word
    
    def remove_suffix(self, word):
        length = len(word)-1
        if(length > 3 and word[length-1:] == "es" and word[length-2] in {"r", "s", "l", "z"}):
            return word[:length-1]
        if(length > 2 and word[length-1:] == "ns"):
            word = word[:length-1] + "m"
            return word
        if(length > 3 and word[length-1:] == "is"):
            if (word[length-2] in {"e", "é"}):
                word = word[:length-2] + "el"
                return word
            if(word[length-2] == "a"):
                word = word[:length-1] + "l"
                return word
            if(word[length-2] == "ó"):
                word = word[:length-2] + "ol"
                return word
            word = word[:length] + "l"
            return word
        if(length > 2 and (word[length-2:] == "ões" or word[length-2:] == "ães")):
            word = word[:length-2] + "ão"
            return word
        if(length > 5 and word[length-4:] == "mente"):
            word = word[:length-4]
            return word
        if(length > 2 and word[length] == "s"):
            word = word[:length]
        return word
    
    def norm_feminin(self, word):
        length = len(word)-1
        if(length < 3 or word[length] != "a"):
            return word
        if(length > 6 and word[length-3:length] in {"inh", "iac", "eir"}):
            word = word = word[:length] + "o"
            return word
        if(length > 5):
            if(word[length-2:length] == "on"):
                word = word[:length-2] + "ão"
                return word
            if(word[length-2:length] == "or"):
                word = word[:length] 
                return word
            if(word[length-2:length] in {"ic", "id", "iv", "ad", "am", "os"}):
                word = word[:length] + "o"
                return word
            if(word[length-2:length] == "es"):
                word = word[:length-2] + "ês"
                return word
            if(word[length-1] == "n"):
                word = word[:length] + "o"
                return word
            return word 
        return word
    