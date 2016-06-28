from dal import autocomplete
from cities_light.models import City
from models import Institution, Person
from django import forms
from django.utils.translation import ugettext_lazy as _


class PersonForm(forms.ModelForm):

    def __init__(self, data=None, *args, **kwargs):
        super(PersonForm, self).__init__(data, *args, **kwargs)
        self.fields['zipcode'].widget.attrs['onBlur'] = 'pesquisacep(this.value);'

    class Meta:
        model = Person
        fields = '__all__'

    class Media:
        js = ('/static/js/cep.js',)


class InstitutionForm(forms.ModelForm):

    city = forms.ModelChoiceField(queryset=City.objects.all(), required=False, label=_('City'),
                                  widget=autocomplete.ModelSelect2(url='city_autocomplete'))

    class Meta:
        model = Institution
        fields = '__all__'
