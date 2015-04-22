from django.conf.urls import patterns, url

from activity import views

urlpatterns = patterns('',
    url(r'^seminars/$', views.seminars_report, name='seminars_report'),
)