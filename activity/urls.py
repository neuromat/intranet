from activity import views
from django.conf.urls import url


urlpatterns = [
    url(r'^seminars/$', views.seminars_report, name='seminars_report'),
    url(r'^training_programs/$', views.training_programs_report, name='training_programs_report'),
    url(r'^meetings/$', views.meetings_report, name='meetings_report'),
    url(r'^seminar_show_titles/$', views.seminar_show_titles, name='seminar_show_titles'),
    url(r'^seminar_latex/$', views.seminar_latex, name='seminar_latex'),
    url(r'^training_programs_latex/$', views.training_programs_latex, name='training_programs_latex'),
]
