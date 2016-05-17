from cities_light.models import City
from dal import autocomplete
from scientific_mission.models import ScientificMission
from django import forms
from django.utils.translation import ugettext_lazy as _


class ScientificMissionForm(forms.ModelForm):

    origin_city = forms.ModelChoiceField(queryset=City.objects.all(), label=_('City of origin'), initial=1383,
                                         widget=autocomplete.ModelSelect2(url='city_autocomplete'))
    destination_city = forms.ModelChoiceField(queryset=City.objects.all(), label=_('City of destination'), initial=1383,
                                              widget=autocomplete.ModelSelect2(url='city_autocomplete'))

    class Meta:
        model = ScientificMission
        fields = '__all__'
        localized_fields = ('amount_paid',)
