from django.conf.urls import patterns, url

from dissemination import views

urlpatterns = patterns('',
    url(r'^dissemination_report/$', views.dissemination_report, name='dissemination_report'),
    url(r'^dissemination_tex/$', views.dissemination_tex, name='dissemination_tex'),
)