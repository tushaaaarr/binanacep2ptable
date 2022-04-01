from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home),
    path('get-advertisments-ajax', views.getAdvertismentsAjax),
    path('submit-comment',views.submitComment,name='submit-comment'),
]