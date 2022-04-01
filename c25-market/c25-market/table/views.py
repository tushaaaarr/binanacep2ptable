from asyncio import constants
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from elasticsearch import Elasticsearch
from constants import ELASTIC_SEARCH_HOST
from table.models import Advertisement
from table.documents import AdvertisementDocument
import json
import hashlib

# Create your views here.

es = Elasticsearch(ELASTIC_SEARCH_HOST)
def getAdvertismentsAjax(request):
    ## comments: retrive from comments doc, store it in dict {advrtiser_no: comment}
    comments = {}
    comments_docs = es.search(index="comments",query={'match_all':{}},size=5000)['hits']['hits']
    for comment in comments_docs:
        comments[comment['_source']['advertiser_no']] = comment['_source']['comment']

    res = es.search(index="advertisements",query={'match_all':{}},size=5000)
    advertisments = list()
    for hit in res['hits']['hits']:
        src = hit["_source"]
        src['comment'] = comments.get(src['advertiser_no'], '')
        advertisments.append(src)

    return JsonResponse(advertisments,safe=False)   

def submitComment(request):
    if request.POST:
        advertiser_no = request.POST.get('advertiser_no') 
        updated_comment = request.POST.get('updated_comment') 
        index = 'comments'
        doc = {'advertiser_no':advertiser_no,
                'comment':updated_comment
                }
        
        query_body = {
            "query": {
                "match": {
                    "advertiser_no":doc['advertiser_no'] 
                    }
                }
            }
        res = es.search(index=index,body = query_body,size=1)

        if res['hits']['total']['value'] == 0 : #no comment present for advertiser_no
            es.index(index=index,document=doc)
        else :
            es.update(index = index ,id = res['hits']['hits'][0]['_id'] ,body={
                            'doc':{'comment': doc['comment']}
                        })
    
    
    return JsonResponse({'status': 1 },safe=False)

def getdata():
    res = es.search(index="advertisements",query={'match_all':{}},size=5000)
    context = {
        'heads':["Exchange","Advertisers","Orders","Completion","Price","Fiat","Payment","Available","Limit", "Comment"],
        'rows':[]
    }
    for hit in res['hits']['hits']:
        src = hit["_source"]
        arr = [src[i] for i in src]
        arr.append("") 
        context['rows'] += [arr]
    return context

def home(request):
    context=getdata()
    return render(request,'table/datatable3.html',context)
