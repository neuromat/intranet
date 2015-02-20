from django.conf.urls import patterns, url

from order import views

urlpatterns = patterns('',
    url(r'^list_order/$', views.list_order, name='list_order'),
)
