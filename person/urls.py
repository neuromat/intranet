from person import views
from django.conf.urls import url


urlpatterns = [
    url(r'^citation_names/$', views.citation_names, name='citation_names'),
    url(r'^researchers/$', views.researchers, name='researchers'),
]
