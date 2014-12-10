from django import forms
from order.models import Investigator
from django.forms import Select
from cep.widgets import CEPInput

class InvestigatorForm(forms.ModelForm):

    class Meta:
        model = Investigator

        fields = ['zipcode', 'street', 'district', 'city', 'state', 'country']

        widgets = {
            'zipcode': CEPInput(address={'street': 'id_street', 'district': 'id_district', 'city': 'id_city',
                                         'state': 'id_state'},
                                       attrs={'pattern': '\d{5}-?\d{3}'}),
            'country': Select(attrs={'class': 'bfh-countries', 'data-country': 'BR'}),
            'state': Select(attrs={'class': 'bfh-states', 'data-country': 'id_country'}),
        }

    class Media:
        js = ('/static/BootstrapFormHelpers/dist/js/bootstrap-formhelpers.min.js',)
        css = {
            'all': ('/static/BootstrapFormHelpers/dist/css/bootstrap-formhelpers.min.css',)
        }