from dissemination import views
from django.conf.urls import url


urlpatterns = [
    url(r'^dissemination_file/$', views.dissemination_file, name='dissemination_file'),
]
