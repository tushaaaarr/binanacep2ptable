# from pyexpat import model
# from async_timeout import timeout
from django.db import models
# from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, Boolean, FacetedSearch
# from elasticsearch_dsl.connections import connections
# from elasticsearch import Elasticsearch
# from constants import ELASTIC_SEARCH_HOST

# Define a default Elasticsearch client
# Elasticsearch(ELASTIC_SEARCH_HOST)
# connections.create_connection(alias='Advertisement', hosts=[ELASTIC_SEARCH_HOST], timeout=60)

# class Advertisement(Document):
#     advertisor = Text()  
#     orders = Text()
#     completion = Text()
#     price = Date()
#     fiat = Text()
#     payment = Text()
#     available = Text()
#     limit = Text()

    # class Index:
    #     name = 'advertisements'
    #     settings = {
    #     }
    # def save(self, **kwargs):
    #     return super(Advertisement, self).save(**kwargs)
        
# Advertisement.init()

class Advertisement(models.Model):
    exchange = models.TextField()
    advertiser_no = models.TextField()
    advertiser = models.TextField()  
    orders =  models.TextField()
    completion =  models.TextField()
    price =  models.TextField()
    fiat =  models.TextField()
    payment =  models.TextField()
    available = models.TextField()
    limit =  models.TextField()
def __str__(self):
    return '%s' % (self.advertiser)

