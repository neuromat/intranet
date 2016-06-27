from dal import autocomplete
from models import ScientificMission, Route
from django import forms


class RouteForm(forms.ModelForm):

    class Meta:
        model = Route
        fields = ('origin_city', 'destination_city', 'departure', 'arrival')
        widgets = {
            'origin_city': autocomplete.ModelSelect2(url='city_autocomplete'),
            'destination_city': autocomplete.ModelSelect2(url='city_autocomplete'),
        }

    class Media:
        css = {
            'all': ('/static/css/inline_autocomplete.css',)
        }


class ScientificMissionForm(forms.ModelForm):

    class Meta:
        model = ScientificMission
        fields = '__all__'
        widgets = {
            'destination_city': autocomplete.ModelSelect2(url='city_autocomplete'),
        }
        localized_fields = ('amount_paid',)
