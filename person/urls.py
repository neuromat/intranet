from person import views
from django.conf.urls import url


urlpatterns = [
    url(r'^researchers/$', views.researchers, name='researchers'),
]
