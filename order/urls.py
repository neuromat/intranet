from django.conf.urls import patterns, url

from order import views

urlpatterns = patterns('',
    url(r'show_institute$', views.show_institute, name='show_institute'),
    url(r'show_department$', views.show_department, name='show_department'),
    url(r'^list_order/$', views.list_order_by_type, name='list_order_by_type'),
    url(r'^additional_options/$', views.select_additional_options, name='selected_additional_options'),
)