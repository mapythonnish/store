# sales_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('userregister', views.storeowner, name='storeowner'),
    path('register/', views.register_store_owner, name='register_store_owner'),
    path('registersalesperson/', views.salesregister, name='register_sales_person'),
    path('loginsales/', views.saleslogin, name='sales_login'),
    path('success_page/', views.thanku, name='success_page'),
    path('storeowner/', views.view_registered_store_owners, name='store_owner'),
    path('error/', views.error, name='error'),
    path('storeusers/', views.storeuser, name='store_user'),
    path('logoutuser/', views.saleslogout, name='logout_user'),
]