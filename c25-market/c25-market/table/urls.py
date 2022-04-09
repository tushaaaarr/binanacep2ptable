from unicodedata import name
from django.urls import path
from . import views, user, administrator
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home),

    path('setup_elastic_search',views.setup_elastic_search,name='create Elastic Search Indices'),

    path('login',views.login,name='Login'),
    path('logout',views.logout,name='logout'),
    path('register',views.register,name='Register'),
    path('verify_magic_link',views.verify_magic_link,name='Verify Magic Link'),

    path('get-advertisments-ajax', views.getAdvertismentsAjax),
    path('submit-comment',views.submitComment,name='submit-comment'),

    # path('generate_magic_link',views.generate_magic_link,name='generate_magic_link'),


    # User/Staff router
    path('user',user.home, name='User Home'),
    
    # Admin router
    path('administrator',administrator.home, name='Admin Home'),
    path('administrator-handling',administrator.AdminPage,name='admin-page'),
    path('get-admin-data',administrator.GetAdminData,name='GetAdminData'),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)