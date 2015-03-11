from django.conf.urls import patterns, url

from order import views

urlpatterns = patterns('',
    url(r'show_institute$', views.show_institute, name='show_institute'),
)