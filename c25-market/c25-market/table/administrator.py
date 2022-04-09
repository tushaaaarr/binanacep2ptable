from django.shortcuts import render,redirect
from elasticsearch import Elasticsearch
from django.http import HttpResponse, JsonResponse
from elasticsearch import Elasticsearch
from constants import ELASTIC_SEARCH_HOST, MAGIC_LINK_MAIL_TEMPLATE
es = Elasticsearch(ELASTIC_SEARCH_HOST)

def checkLogin(request): 
    if(request.session.get('user') == None or request.session.get('user')['role'] != 'admin'):
        return False

def home(request):
    if checkLogin(request) == False:
        return redirect('/login')
    return render(request,'table/datatable3.html')

def AdminPage(request):
    index = 'users'
    users_data = {}
    user_list = list()
    query_body = {
        "query": {
            "match": {
                "role":'user' 
                }
            }
        }
    res = es.search(index=index,body=query_body,size=5000)
    for hit in res['hits']['hits']:
        src = hit["_source"]
        src['user_id']= hit['_id']
        user_list.append(src)
    context = {'users':user_list}
    return render(request,'admin_base/index.html',context)

def GetAdminData(request):
    if request.POST:
        user_id = request.POST.get('user_id')
        status = request.POST.get('status')
        if status == '1':
            # update users-status 
            es.update(index = 'users' ,id = user_id ,body={
                            'doc':{'status': 1}
            })
        else:
            # update users-status 
            es.update(index = 'users' ,id = user_id ,body={
                            'doc':{'status': 0}
                        })

    return HttpResponse(' ')
