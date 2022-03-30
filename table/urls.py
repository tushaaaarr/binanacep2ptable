from django.urls import path
from . import views

urlpatterns = [
    path('',views.home),
    path('get_advertisments_ajax', views.get_advertisments_ajax)
]