from django.conf.urls import url
from . import views

app_name="travelbuddy"

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^travels$', views.travels, name='travels'),
    url(r'^trip_add$', views.trip_add, name='trip_add'),
    url(r'^join_trip/(?P<trip_id>\d+)$', views.join_trip, name='join_trip'),
    url(r'^destination/(?P<id>\d+)$', views.destination, name='destination'),
    url(r'^create_trip$', views.create_trip, name='create_trip'),
]
