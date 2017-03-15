from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

class Termizer:
    def __init__(self):
        self.stop = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self.tokenizer = RegexpTokenizer(r"\w+")
        pass

    def getTermsList(self,str):
        tokens = self.tokenizer.tokenize(str)
        words = [token for token in tokens if token not in self.stop and token.isdigit() == False]
        terms = [self.stemmer.stem(word) for word in words]
        return terms

    def getTermsAndStopList(self,str):
        stopwords = []
        words = []
        tokens = self.tokenizer.tokenize(str)
        for token in tokens:
            if token.isdigit() == False:
                if token not in self.stop:
                    words.append(token)
                else:
                    stopwords.append(token)
        terms = [self.stemmer.stem(word) for word in words]
        return terms, stopwords
