import json
class DocDataBase:
    """
    a data base can read json copus and build data for query by key
    """
    def __init__(self, path):
        with open(path, 'r') as file:
            self.data = json.load(file)

    def lookup(self, key):
        res = None
        try:
            res = self.data[str(key)]
        finally:
            return res