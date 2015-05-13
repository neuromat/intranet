from django.conf.urls import patterns, url

from research import views

urlpatterns = patterns('',
    url(r'^published/$', views.published_articles, name='published_articles'),
)
