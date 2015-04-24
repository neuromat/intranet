from django.conf.urls import patterns, url

from activity import views

urlpatterns = patterns('',
    url(r'^seminars/$', views.seminars_report, name='seminars_report'),
    url(r'^training_programs/$', views.training_programs_report, name='training_programs_report'),
    url(r'^meetings/$', views.meetings_report, name='meetings_report'),
)