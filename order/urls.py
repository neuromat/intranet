from django.conf.urls import patterns, url

from order import views

urlpatterns = patterns('',
    url(r'^list_order/$', views.list_order_by_type, name='list_order_by_type'),
)
