from django.shortcuts import render,redirect
from elasticsearch import Elasticsearch

def checkLogin(request): 
    if(request.session.get('user') == None or request.session.get('user')['role'] != 'admin'):
        return False

def home(request):
    if checkLogin(request) == False:
        return redirect('/login')
    return render(request,'table/datatable3.html')

