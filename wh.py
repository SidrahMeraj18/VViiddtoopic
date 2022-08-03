from ast import keyword
import os
from click import Path
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
import sys
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir
from icecream import ic
def createSearchableData(root,keywordToSearch):   
    schema = Schema(title=TEXT(stored=True),path=ID(stored=True),\
              content=TEXT,textdata=TEXT(stored=True))
    if not os.path.exists("indexdir1"):
        os.mkdir("indexdir1")
    ix = create_in("indexdir1",schema)
    writer = ix.writer()
    path = root 
    fp = open(path,'r')
    print(path)
    text = fp.read()
    writer.add_document(title=path.split("/")[0], path=path,\
        content=text,textdata=text)
    fp.close()
    writer.commit()
    ix = open_dir("indexdir1")
    query_str = keywordToSearch
    with ix.searcher(weighting=scoring.Frequency) as searcher:
        query = QueryParser("content", ix.schema).parse(query_str)
        results = searcher.search(query,limit=1)
        if len(results) != 0:
            return True 
        else:
            return False