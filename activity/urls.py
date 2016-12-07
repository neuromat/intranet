from activity import views
from django.conf.urls import url


urlpatterns = [
    url(r'^seminar_show_titles/$', views.seminar_show_titles, name='seminar_show_titles'),
    url(r'^training_programs_latex/$', views.training_programs_latex, name='training_programs_latex'),

    #  reports
    url(r'^seminar_report/$', views.seminar_report, name='seminar_report'),
]
