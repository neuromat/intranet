from scientific_mission.models import ScientificMission
from cities_light.models import Country, City
from django import forms
from django.forms import Select
from django.utils.translation import ugettext_lazy as _


class ScientificMissionForm(forms.ModelForm):

    origin_country = forms.ModelChoiceField(Country.objects.all(), label=_('Country of origin'), initial=31,
                                            widget=Select(attrs={'onchange': 'load_origin_cities(this.value);'}))
    origin_city = forms.ModelChoiceField(City.objects.all(), label=_('City of origin'))
    destination_country = forms.ModelChoiceField(Country.objects.all(), label=_('Country of destination'), initial=31,
                                                 widget=Select(attrs={'onchange': 'load_destination_cities(this.value);'}))
    destination_city = forms.ModelChoiceField(City.objects.all(), label=_('City of destination'), initial=1383)

    class Meta:
        model = ScientificMission
        localized_fields = ('amount_paid',)

    class Media:
        js = ('/static/js/load_cities.js',)
