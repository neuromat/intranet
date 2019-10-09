from django.conf.urls import url
from activity import views


urlpatterns = [
    url(r'^seminars_show_titles/$', views.seminars_show_titles, name='seminars_show_titles'),

    #  files
    url(r'^seminars_file/$', views.seminars_file, name='seminars_file'),
    url(r'^training_programs_file/$', views.training_programs_file, name='training_programs_file'),
]
