from django.conf.urls import patterns, url
from scientific_mission import views


urlpatterns = patterns('',
                       url(r'^load_origin_cities/$', views.load_origin_cities, name='load_origin_cities'),
                       url(r'^load_destination_cities/$', views.load_destination_cities,
                           name='load_destination_cities'),
                       )