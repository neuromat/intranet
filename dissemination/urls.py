from django.conf.urls import patterns, url

from dissemination import views

urlpatterns = patterns('',
    url(r'^dissemination_report/$', views.dissemination_report, name='dissemination_report'),
)