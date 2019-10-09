from django.conf.urls import url
from scientific_mission import views


urlpatterns = [
    url(r'^city_autocomplete/$', views.CityAutocomplete.as_view(), name='city_autocomplete'),
    url(r'^show_missions/$', views.mission_show_titles, name='anexo_missions'),

    #  reports
    url(r'^scientific_missions_file/$', views.missions_file, name='scientific_missions_file'),
]
