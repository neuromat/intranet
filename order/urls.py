from django.conf.urls import patterns, url

from order import views

urlpatterns = patterns('',
    url(r'^list_order/$', views.list_order_by_type, name='list_order_by_type'),
    url(r'^additional_options/$', views.select_additional_options, name='selected_additional_options'),
    url(r'^scientific_missions/$', views.scientific_missions_report, name='scientific_missions_report'),
)