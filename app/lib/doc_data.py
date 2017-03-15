class DocData:
    def __init__(self, posting, doc):
        """
        :param posting: read a posting number and doc from json data, build a posting-document data
        """
        self.posting = posting
        self.title = doc["title"]
        self.director = doc["director"]
        self.starring = "/".join(doc["starring"])
        self.runtime = doc["runtime"]
        self.language = doc["language"]
        self.country = doc["country"]
        self.abstract = doc["text"][:350]
        self.text = doc["text"]

    def setSimilarity(self,similarity):
        self.similarity = similarity


