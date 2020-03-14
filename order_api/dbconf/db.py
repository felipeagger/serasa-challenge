#Dependencies
from os import getenv
from elasticsearch import Elasticsearch


#ElasticSearch Conection
def config_db():
    try:
        es = Elasticsearch("http://"+getenv('ELASTIC')+":9200") 
        print('Connected to ElasticSearch')
    except:
        print('Exiting because ElasticSearch not Connected!')
        exit(1)

    #Create Index Orders
    es.indices.create(index='orders', ignore=400)

    return es