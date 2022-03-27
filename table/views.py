from asyncio import constants
from django.http import HttpResponse
from django.shortcuts import render
from elasticsearch import Elasticsearch
from constants import ELASTIC_SEARCH_HOST
from table.models import Advertisement
from table.documents import AdvertisementDocument
# Create your views here.

es = Elasticsearch(ELASTIC_SEARCH_HOST)
def getdata():
    res = es.search(index="advertisements",query={'match_all':{}},size=50)
    context = {
        'heads':["Advertisors","Orders","Completion","Price","Fiat","Payment","Available","Limit"],
        'rows':[]
    }
    for hit in res['hits']['hits']:
        src = hit["_source"]
        context['rows'] += [[src[i] for i in src]]
    # print(context,len(context['rows']))
    return context

def home(request):
    # ad = Advertisement(
    #      advertisor = "akash",
    #      orders = 555
    # )
    # ad.save()
    context=getdata()
    return render(request,'table/datatable.html',context)