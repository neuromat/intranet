from dissemination import views
from django.conf.urls import url


urlpatterns = [
    url(r'^dissemination_report/$', views.dissemination_report, name='dissemination_report'),
    url(r'^dissemination_tex/$', views.dissemination_tex, name='dissemination_tex'),
]
