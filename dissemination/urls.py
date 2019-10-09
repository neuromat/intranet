from django.conf.urls import url
from dissemination import views


urlpatterns = [
    url(r'^dissemination_file/$', views.dissemination_file, name='dissemination_file'),
]
