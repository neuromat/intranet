from django.conf.urls import patterns, url

from research import views

urlpatterns = patterns('',
    url(r'^articles/$', views.articles, name='articles'),
    url(r'^academic_works/$', views.academic_works, name='academic_works'),
    url(r'^academic_works_tex/$', views.academic_works_tex, name='academic_works_tex'),
    url(r'^import_papers/$', views.import_papers, name='import_papers'),
    url(r'^add_periodicals/$', views.add_periodicals, name='add_periodicals'),
    url(r'^add_papers/$', views.add_papers, name='add_papers'),
    url(r'^add_periodical_papers/$', views.add_periodical_papers, name='add_periodical_papers'),
)