from django.shortcuts import render,redirect
from elasticsearch import Elasticsearch


def checkLogin(request):
    if(request.session.get('user') == None or request.session.get('user')['role'] != 'user'):
        return False

def home(request):
    if checkLogin(request) == False:
        return redirect('/login')
    return render(request,'user/advertisement.html')

