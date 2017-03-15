import shelve
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class TfIdfDataBase:
    """
    a data base that can read seralized shelves data and build a index for lookup
    """
    def __init__(self,path):
        self.tf_idf_database = shelve.open(path, writeback=False)

    def lookup(self, key):
        """
        :param key: a term to lookup
        :return: a list of postings
        """
        res = None
        try:
            res = self.tf_idf_database[str(key)]
        finally:
            return res

    def save(self, data):
        for item in data:
            self.tf_idf_database[str(item)] = data[item]