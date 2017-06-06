from django.conf.urls import url
from django.contrib import admin
from . import views

#app_name='login_app'
urlpatterns =[
    #url(r'^$', views.index, name='index'),
    url(r'^registration$', views.log_register, name='register'),
    url(r'^login$', views.log_register, name='login'),
    url(r'^logout$', views.logout, name='logout'),

]
