from django.conf.urls import patterns, url
from scientific_mission import views


urlpatterns = patterns('',
                       url(r'^load_origin_cities/$', views.load_origin_cities, name='load_origin_cities'),
                       url(r'^load_destination_cities/$', views.load_destination_cities,
                           name='load_destination_cities'),
                       url(r'^report/$', views.missions_report, name='missions_report'),
                       url(r'^scientific_missions_tex/$', views.missions_tex, name='scientific_missions_tex'),
                       )
