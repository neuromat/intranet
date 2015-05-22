from django import forms
from custom_user.models import Person
from cep.widgets import CEPInput


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person

        fields = ['zipcode', 'street', 'district', 'city', 'state']

        widgets = {
            'zipcode': CEPInput(address={'street': 'id_street', 'district': 'id_district', 'city': 'id_city',
                                         'state': 'id_state'}, attrs={'pattern': '\d{5}-?\d{3}'}),
        }