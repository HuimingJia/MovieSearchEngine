import math
import os
from flask import *
import urllib
from app import app
from app.db.index_database import IndexDataBase
from app.db.doc_database import DocDataBase
from app.db.idf_database import IdfDataBase
from app.db.tf_idfweightdatabase import TfIdfDataBase
from app.lib.termizer import Termizer
from app.lib.engine import Engine
from app.lib.doc_data import DocData

systempath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
engine = Engine(IndexDataBase(systempath + "/data/data.db"), DocDataBase(systempath + "/data/2016_movies_standard.json"),IdfDataBase(systempath + "/data/idf.db"),
                TfIdfDataBase(systempath + "/data/tf_idf.db"))

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route('/results', methods=['GET'])
def results():
    """
    :return: a tenplate show the rearching result
     this function will get the paremeters of query and page number, and return specific number of result and statue of page information and query infromation
     query: wrapped url
     textL: query text
     total: total search result
     pages: number of pages
     current: current page in whole result
     termslist: a list of term that would be searched in engine
     stopwords: a list of term that not be searched in engine
     strangeterm: the term that have no searc result
     res: search result
    """
    text = str(request.args.get('query')).strip()
    current_page = int(request.args.get('page'))

    if text == "" or text == None:
        return render_template('index.html')
    termizer = Termizer()
    termslist, stopwords = termizer.getTermsAndStopList(text)
    postings, strangeterm = engine.intersect(termslist)

    if postings == None or len(postings) == 0:
        return render_template('results.html', query=urllib.quote_plus(text), text=text, total=(len(postings)),
                               pages=0, current=current_page,
                               termslist=", ".join(termslist), stopwords=", ".join(stopwords),
                               strangeterm=strangeterm, res=[])

    items_page = 10
    res = []
    start = (current_page - 1) * items_page
    end = start + items_page

    for posting in postings[start : end]:
        doc = DocData(posting[1], engine.search(posting[1]))
        doc.setSimilarity(posting[0])
        res.append(doc)

    for item in res:
        if item.title == "" or item.title == None:
            item.title = "EMPTY TITLE"
    pages = int(math.ceil(len(postings) / float(items_page)))
    return render_template('results.html', query = urllib.quote_plus(text), text =text, total=(len(postings)), pages=pages, current = current_page,
                           termslist=", ".join(termslist), stopwords=", ".join(stopwords), strangeterm = strangeterm, res = res)


@app.route('/<posting>')
def showdetail(posting):
    """
    :param posting: posting of a article
    :return: the content of this article
    """
    print "@app.route", posting
    doc = DocData(posting, engine.search(posting))
    return render_template('article.html', doc = doc)