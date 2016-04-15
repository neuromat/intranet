from django.conf.urls import patterns, url

from person import views

urlpatterns = patterns('',
    url(r'^citation_names/$', views.citation_names, name='citation_names'),
)