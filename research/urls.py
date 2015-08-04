from django.conf.urls import patterns, url

from research import views

urlpatterns = patterns('',
    url(r'^published_or_accepted/$', views.published_articles, name='published_articles'),
    url(r'^academic_works/$', views.academic_works, name='academic_works'),
)