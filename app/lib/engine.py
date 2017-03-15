from cmath import log
import heapq
class Engine:
    def __init__(self, index, data, idf, tf_idf):
        """
        :param index: search index and doc data
        """
        self.index = index
        self.data = data
        self.idf = idf
        self.tf_idf = tf_idf

    def intersect(self, termslist):
        """
        :param termslist: a list of terms to lookup
        :return: a list of postings of searching result with similarity
        this function will get list for very term and intersect them by optimized algorithm
        intersect the list from shortest one, and when intersecting the postings, we use two points
        and then rank the postings by the cosine similarity
        """
        postings = []
        tf_idf_query = {}
        termslist = list(set(termslist))

        if len(termslist) == 0:
            return [], None

        for term in termslist:
            if self.index.lookup(str(term)) == None:
                return [], str(term)

        for term in termslist:
            postings.append(self.index.lookup(str(term)))

        # sort according to the length of the list
        for i in range(len(postings)):
            for j in range(len(postings) - i - 1):
                if(len(postings[j]) > len(postings[j + 1])):
                    temp = postings[j]
                    postings[j] = postings[j + 1]
                    postings[j + 1] = temp

        # intersection of postings lists, start from the shortest one, and use two pointer when compare two list
        # after finish every comparsion, assign the new intersected postings list to the res
        res = postings[0]

        for count in range(1,len(postings)):
            temp = []
            point_res = point_postings = 0
            while point_res < len(res) and point_res < len(postings[count]):
                if res[point_res] == postings[count][point_postings]:
                    temp.append(res[point_res])
                    point_postings = point_postings + 1
                    point_res = point_res + 1
                elif res[point_res] > postings[count][point_postings]:
                    point_postings = point_postings + 1
                else:
                    point_res = point_res + 1
            res = temp

        #compute tf_idf weight for query
        for term in termslist:
            tf_idf_query[term] = 0
        for term in termslist:
            tf_idf_query[term] = tf_idf_query[term] + 1

        for term in tf_idf_query:
            tf_idf_query[term] = (1 + log(tf_idf_query[term])).real * self.idf.lookup(str(term))

        #rank the posting list and get the first 30 posting
        res = self.rank(res,tf_idf_query)
        return res, None

    def searchlist(self, postings):
        """
        :param postings: a lists of postings to lookup
        :return: a list of docments
        """
        res = []
        for posting in postings:
            res.append(self.data.lookup(str(posting)))
        return res

    def search(self, posting):
        """
        :param posting: a single posting to lookup
        :return: a single result document
        """
        return self.data.lookup(str(posting))

    def rank(self,res,tf_query):
        """
        :param res: the result postings for all query terms
        :param tf_query: the tf weight for the every query term
        :return: ranked top 30 result postings
        """
        rank = {}
        heap = []

        for item in res:
            rank[item] = 0

        for term in tf_query:
            for item in res:
                dict = self.tf_idf.lookup(item)
                rank[item] = rank[item] + tf_query[term] * dict[str(term)]

        #using min head to sort the pair(similarity, posting)
        res = []
        for item in rank:
            heapq.heappush(heap, (rank[item].real, item))

        for i in range(len(heap)):
            res.append(heapq.heappop(heap))

        #reverse the list to make the ranked list order in ascending order
        res.reverse()
        return res[:30]