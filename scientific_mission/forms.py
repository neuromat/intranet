from dal import autocomplete
from models import ScientificMission, Route
from django import forms

from person.models import Person


class ProcessField(forms.CharField):

    def to_python(self, value):
        # Return an empty list if no input was given.
        return value

    def validate(self, value):
        """Check if value consists only of valid emails."""
        # Use the parent's handling of required fields, etc.
        super(ProcessField, self).validate(value)

    def clean(self, value):
        return value


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


class AnnexSevenForm(forms.Form):

    person = forms.ModelChoiceField(queryset=Person.objects.all(), empty_label="----------", required=True)
    value = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    process = ProcessField(widget=forms.TextInput(attrs={'placeholder': '0000/00000-0'}))

    def clean(self):
        cleaned_data = super(AnnexSevenForm, self).clean()
        person = cleaned_data.get('person')
        value = cleaned_data.get('value')
        process = cleaned_data.get('process')
