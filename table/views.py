from asyncio import constants
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from elasticsearch import Elasticsearch
from constants import ELASTIC_SEARCH_HOST
from table.models import Advertisement
from table.documents import AdvertisementDocument
# Create your views here.

es = Elasticsearch(ELASTIC_SEARCH_HOST)
def get_advertisments_ajax(request):
    res = es.search(index="advertisements",query={'match_all':{}},size=5000)
    context = {
        'heads':["Exchange","Advertisors","Orders","Completion","Price","Fiat","Payment","Available","Limit","Comment"],
        'rows':[]
    }
    for hit in res['hits']['hits']:
        src = hit["_source"]
        arr = [src[i] for i in src]
        arr.append("") #commment
        arr.append('<button class="edit" type="button">Edit</button>')
        context['rows'] += [arr]
        # context['rows'].append(" ")
    # print(context,len(context['rows']))
    return JsonResponse(context)


def getdata():
    res = es.search(index="advertisements",query={'match_all':{}},size=5000)
    context = {
        'heads':["Exchange","Advertisers","Orders","Completion","Price","Fiat","Payment","Available","Limit"],
        'rows':[]
    }
    for hit in res['hits']['hits']:
        src = hit["_source"]
        arr = [src[i] for i in src]
        # arr.append("") #commment
        # arr.append('<button class="edit" type="button">Edit</button>')
        context['rows'] += [arr]
        # context['rows'].append(" ")
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