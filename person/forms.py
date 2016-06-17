from dal import autocomplete
from cep.widgets import CEPInput
from cities_light.models import City
from models import Institution, Person
from django import forms
from django.utils.translation import ugettext_lazy as _


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person

        fields = ['zipcode', 'street', 'district', 'city', 'state']

        widgets = {
            'zipcode': CEPInput(address={'street': 'id_street', 'district': 'id_district', 'city': 'id_city',
                                         'state': 'id_state'}, attrs={'pattern': '\d{5}-?\d{3}'}),
        }


class InstitutionForm(forms.ModelForm):

    city = forms.ModelChoiceField(queryset=City.objects.all(), required=False, label=_('City'),
                                  widget=autocomplete.ModelSelect2(url='city_autocomplete'))

    class Meta:
        model = Institution
        fields = '__all__'
