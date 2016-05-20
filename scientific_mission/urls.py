from scientific_mission import views
from django.conf.urls import url


urlpatterns = [
    url(r'^report/$', views.missions_report, name='missions_report'),
    url(r'^scientific_missions_tex/$', views.missions_tex, name='scientific_missions_tex'),
    url(r'^city_autocomplete/$', views.CityAutocomplete.as_view(), name='city_autocomplete'),
]
