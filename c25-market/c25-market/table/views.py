from asyncio import constants
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from elasticsearch import Elasticsearch
from constants import ELASTIC_SEARCH_HOST, MAGIC_LINK_MAIL_TEMPLATE
from table.models import Advertisement
from table.documents import AdvertisementDocument
import json
import hashlib
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User 
from datetime import datetime,timezone,timedelta
import hashlib
import random
import string
from django.core import mail
from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings
import os
from dotenv import load_dotenv
load_dotenv('.env')

# Create your views here.
es = Elasticsearch(ELASTIC_SEARCH_HOST)

def getAdvertismentsAjax(request):
    comments = {}
    comments_docs = es.search(index="comments",query={'match_all':{}},size=5000)['hits']['hits']
    for comment in comments_docs:
        comments[comment['_source']['advertiser_no']] = comment['_source']['comment']

    res = es.search(index="advertisements",query={'match_all':{}},size=5000)
    advertisments = list()
    sr_no = 1
    for hit in res['hits']['hits']:
        src = hit["_source"]
        src['sr_no'] = sr_no
        src['comment'] = comments.get(src['advertiser_no'], '')
        advertisments.append(src)
        sr_no+=1

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
    return redirect('/login')
    context=getdata()
    return render(request,'table/datatable3.html',context)


# Auth 
def login(request):
    # print(SMTP_HOST, SMTP_HOST_PORT, SMTP_HOST_USER, SMTP_HOST_PASS )
    # # for k, v in sorted(os.environ.items()):
    # #     print(k+':', v)
    # #     print('\n')
    if request.session.get('user') != None:
        return redirect(f"/{request.session.get('user')['role']}")
    page_data = {}
    page_data['admin_email'] = str(os.getenv('ADMIN_EMAIL'))
    page_data['page_name'] = "auth/login.html"
    page_data['title'] = "Login"
    page_data['error'] = ''
    page_data['error_mail'] = ''
    
    if request.POST:
        email = request.POST.get('email')
        user_details = get_user(email)
        if user_details == False:
            page_data['error'] = "Email Not Registered"
        elif user_details['status'] == 0:
            page_data['error'] = "Your Account is Not Verified, Please Contact Admin"
        elif user_details['role'] == "admin":
            if request.POST.get('password') != user_details['password']:
                page_data['error'] = "Wrong Password"
            else:
                session_data = {
                    'first_name': user_details['first_name'],
                    'last_name': user_details['last_name'],
                    'email': user_details['email'],
                    'role': 'admin',
                }
                request.session['user'] = session_data
                request.session.set_expiry(60*60) #1 hour
                return redirect('/administrator')
        else:
            #generate magic link and send mail
            magic_link = generate_magic_link()
            save_magic_link(magic_link, email)
            host = 'http://'+request.get_host()
            page_data['error_mail'] = send_magic_link_mail(host, magic_link, email)

        page_data['page_name'] = "auth/login_post.html"
    return render(request,'auth/index.html', {'page_data':page_data})

def logout(request):
    request.session.clear()
    return redirect('/login')

def register(request):
    if request.session.get('user') != None:
        return redirect(f"/{request.session.get('user')['role']}")
    page_data = {}
    page_data['title'] = "Register"
    page_data['page_name'] = "auth/register.html"

    if request.POST:
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')

        user_details = get_user(email)
        if user_details != False:
            page_data['already_registered'] = True
        else:
            doc = {
                'first_name':firstname,
                'last_name':lastname,
                'email':email,
                'status' : 0,
                'role':'user',
                }
            es.index(index = 'users', document=doc)
        page_data['page_name'] = "auth/register_post.html"
    return render(request,'auth/index.html', {'page_data': page_data})

def get_user(email):
    index = 'users'
    res = es.search(index=index,query={'match':{'email': email}},size=1)
    if  res['hits']['total']['value'] == 0:
        return False
    return res['hits']['hits'][0]['_source']
    # return False
def AdminPage(request):
    index = 'users'
    users_data = {}
    user_list = list()
    res = es.search(index=index,query={'match_all':{}},size=5000)
    for hit in res['hits']['hits']:
        src = hit["_source"]
        src['id']= hit['_id']
        user_list.append(src)
    context = {'users_list':user_list}
    return render(request,'admin_base/index.html',context)

def GetAdminData(request):
    if request.POST:
        request.POST.get('status')
        user_id = request.POST.get('user_id')
        status = request.POST.get('status')
        if status == 'True':
            # update users-status 
            es.update(index = 'users' ,id = user_id ,body={
                            'doc':{'status': 1}
            })
        else:
            # update users-status 
            es.update(index = 'users' ,id = user_id ,body={
                            'doc':{'status': 0}
                        })
    index = 'users'
    users_data = {}
    user_list = list()
    res = es.search(index=index,query={'match_all':{}},size=5000)
    for hit in res['hits']['hits']:
        src = hit["_source"]
        src['id']= hit['_id']
        user_list.append(src)
    user_data = ' '
    
    for i in user_list:
        if i['status']==1:
            temp = f"<tr><td class='user_email'>{i['email']}</td><td class='user_id'>{i['status']}</td><td><input class='checkuser' type='checkbox' value='' onchange='CheckBoxClicked({i['id']})'></td></tr>"
        else:
            temp = f"<tr><td class='user_email'>{i['email']}</td><td class='user_id'>{i['status']}</td><td><input class='checkuser' type='checkbox' value='' onchange='CheckBoxClicked({i['id']})'></td></tr>"
        user_data = user_data + temp
        temp = ' '
            
    return JsonResponse({'users_list':user_data})
def verify_magic_link(request):
    page_data = {}
    page_data['title'] = "Magic Link"
    page_data['page_name'] = "auth/magic_link.html"
    page_data['error'] = "Magic Link Required"
    magic_link = request.GET.get('magic_link')

    if magic_link:
        link_data = get_magic_link_data(magic_link)
        if link_data == False:
            page_data['error'] = "Wrong Magic Link, Please Generate Again"
        elif link_data['link_expire_time'] < str(datetime.now()) or link_data['is_used'] == True:
            page_data['error'] = "Magic Link Expired, Please Generate Again"
        else :
            session_data = {
                'magic_link': link_data['magic_link'],
                'first_name': link_data['user']['first_name'],
                'last_name': link_data['user']['last_name'],
                'email': link_data['user']['email'],
                'role': link_data['user']['role'],
            }
            request.session['user'] = session_data
            request.session.set_expiry(60*60) #1 hour
            mark_magic_link_used(magic_link)  
            print(session_data)  
            return redirect(f"/{session_data['role']}")
    return render(request,'auth/index.html', {'page_data': page_data})

def get_magic_link_data(magic_link):
    index = 'magic_links'
    res = es.search(index=index,query={'match':{'magic_link': magic_link}},size=1)
    if  res['hits']['total']['value'] == 0:
        return False
    
    link_data = res['hits']['hits'][0]['_source']
    link_data['user'] = get_user(link_data['user_email'])
    return link_data


def generate_magic_link():
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(20))
    random_string+= str(datetime.now())
    hashed_string = hashlib.sha256(random_string.encode('utf-8')).hexdigest()
    return hashed_string


def save_magic_link(magic_link,email):
    doc = {
        'magic_link':magic_link,
        'link_expire_time':datetime.now() + timedelta(seconds=600),
        'user_email':email,
        'is_used':False,
    }
    es.index(index = 'magic_links',document = doc)

def mark_magic_link_used(magic_link):
    q = {
        "script": {
            "inline": "ctx._source.is_used=true",
            "lang": "painless"
        },
        "query": {
            "match": {
                "magic_link": magic_link
            }
        }
    }
    es.update_by_query(body=q, index='magic_links')

   
def send_magic_link_mail(host ,magic_link, email):
    mail_subject = "Magic Link for Login"
    mail_from = settings.SMTP_HOST_USER
    mail_body = MAGIC_LINK_MAIL_TEMPLATE.replace("{{{MAGIC_LINK_URL}}}",host+'/verify_magic_link?magic_link='+magic_link) 
    try:   
        con = mail.get_connection()
        con.open()
        msg = mail.EmailMessage(
                subject=mail_subject,
                body=mail_body,
                from_email=mail_from,
                to=[email],
                connection=con
            )
        msg.content_subtype = 'html'
        msg.send()
        con.close()
        return ''

    except Exception as _error:
        return format(_error)

def setup_elastic_search(request):
    ADMIN_EMAIL= str(os.getenv('ADMIN_EMAIL'))
    ADMIN_PASS= str(os.getenv('ADMIN_PASS'))
    ADMIN_FIRST_NAME= str(os.getenv('ADMIN_FIRST_NAME'))
    ADMIN_LAST_NAME= str(os.getenv('ADMIN_LAST_NAME'))


    indices = ['users', 'magic_links']
    for indice in indices:
        if es.indices.exists(index=indice):
            pass
        else:
            es.indices.create(index=indice)
    admin_details = {
        'email': ADMIN_EMAIL,
        'password': ADMIN_PASS,
        'first_name': ADMIN_FIRST_NAME,
        'last_name': ADMIN_LAST_NAME,
        'status': 1,
        'role': 'admin'
    }
    es.index(index='users',id=1,document=admin_details)
    return HttpResponse('Done')