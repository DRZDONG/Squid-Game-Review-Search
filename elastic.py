import pathlib
import os
import tokenizer
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'post': 9200}])
FIRST_INDEX = False


def search(query):
    val = es.indices.get_alias(index=['doc_index_1']).keys()
    docs = tokenizer.token_document()
    if "doc_index_1" not in val:
        es.indices.create(index='doc_index_1', ignore=400)
        for doc_id, content in docs.items():
            # metadata = {
            #     "index": {
            #         "_index": 'doc_index_1',
            #         "_id": doc_id,
            #     },
            #     "content": content[0]
            # }
            # data.append(metadata)
            es.index(index='doc_index_1', id=doc_id, body={
                "content": content[0]
            })

    res = es.search(index="doc_index_1", body={
        "query": {
            "match": {
                "content": query
            }
        },
        "size": 50
    })

    lists = []
    for hit in res["hits"]["hits"]:
        id_doc = int(hit['_id'])
        row = []
        user_name = docs[id_doc][1]
        title = docs[id_doc][2]
        rating = docs[id_doc][3]
        date = docs[id_doc][4]
        review_body = docs[id_doc][5]

        row.append(user_name)
        row.append(title)
        row.append(rating)
        row.append(date)
        row.append(review_body)
        lists.append(row)
    return lists


def exact_match_search(query):
    docs = tokenizer.token_document()
    val = es.indices.get_alias(index=['exact']).keys()
    if "exact" not in val:
        es.indices.create(index='exact', ignore=400)
        for doc_id, content in docs.items():

            es.index(index='exact', id=doc_id, body={
                "content": content[0]
            })

    # es.bulk(index="exact", body=data)

    res = es.search(index="exact", body={
        "query": {
            "match_phrase": {
                "content": query
            }
        },
        "size": 50
    })

    # print(len(docs))
    # print(docs.keys())
    lists = []
    # print(res.keys())
    # print(res['hits'].keys())
    for hit in res["hits"]["hits"]:
        id_doc = int(hit['_id'])
        print(id_doc)
        row = []
        user_name = docs[id_doc][1]
        title = docs[id_doc][2]
        rating = docs[id_doc][3]
        date = docs[id_doc][4]
        review_body = docs[id_doc][5]

        row.append(user_name)
        row.append(title)
        row.append(rating)
        row.append(date)
        row.append(review_body)
        lists.append(row)
    return lists
