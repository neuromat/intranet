from scientific_mission import views
from django.conf.urls import url


urlpatterns = [
    url(r'^city_autocomplete/$', views.CityAutocomplete.as_view(), name='city_autocomplete'),
    url(r'^show_missions/$', views.mission_show_titles, name='anexo_missions'),

    #  reports
    url(r'^scientific_missions_tex/$', views.missions_tex, name='scientific_missions_tex'),
    url(r'^scientific_missions_pdf/$', views.missions_pdf, name='scientific_missions_pdf'),

]
