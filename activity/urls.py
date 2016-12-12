from activity import views
from django.conf.urls import url


urlpatterns = [
    url(r'^seminars_show_titles/$', views.seminars_show_titles, name='seminars_show_titles'),
    url(r'^training_programs_latex/$', views.training_programs_latex, name='training_programs_latex'),

    #  files
    url(r'^seminars_file/$', views.seminars_file, name='seminars_file'),
]
