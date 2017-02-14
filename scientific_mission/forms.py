from configuration.models import ProcessNumber
from dal import autocomplete
from models import ScientificMission, Route
from django import forms
from django.utils.translation import ugettext_lazy as _
from person.models import Person

from helpers.forms.date_range import DateInput


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


class AnnexSixForm(forms.Form):

    process = ProcessNumber.get_solo()

    daily_stipend = forms.ModelChoiceField(label=_('Diaria'), queryset=ScientificMission.objects.all(),
                                           empty_label="----------", required=True)
    process = ProcessField(label=_('Process'), widget=forms.TextInput(attrs={'placeholder': process.process_number}))

    def clean(self):
        cleaned_data = super(AnnexSixForm, self).clean()
        daily_stipend = cleaned_data.get('daily_stipend')
        process = cleaned_data.get('process')


class AnnexSevenForm(forms.Form):

    process = ProcessNumber.get_solo()

    period = forms.DateField(label=_('Period'), widget=DateInput, required=False)
    stretch = forms.CharField(label=_('Stretch'), required=True)
    reimbursement = forms.CharField(label=_('Reimbursement'), required=True)
    reason = forms.CharField(label=_('Reason'), required=True)
    person = forms.ModelChoiceField(label=_('Person'), queryset=Person.objects.all(),
                                    empty_label="----------", required=True)
    value = forms.DecimalField(label=_('Value'), max_digits=10, decimal_places=2, required=True)
    process = ProcessField(label=_('Process'), widget=forms.TextInput(
        attrs={'placeholder': process.process_number}))

    def clean(self):
        cleaned_data = super(AnnexSevenForm, self).clean()
        person = cleaned_data.get('person')
        value = cleaned_data.get('value')
        process = cleaned_data.get('process')


class AnnexNineForm(forms.Form):

    process = ProcessNumber.get_solo()

    job = forms.CharField(label=_('Job'), required=True)
    person = forms.ModelChoiceField(label=_('Service provider'), queryset=Person.objects.all(),
                                    empty_label="----------", required=True)
    value = forms.DecimalField(label=_('Value'), max_digits=10, decimal_places=2, required=True)
    process = ProcessField(label=_('Process'), widget=forms.TextInput(
        attrs={'placeholder': process.process_number}))

    def clean(self):
        cleaned_data = super(AnnexNineForm, self).clean()
        person = cleaned_data.get('person')
        value = cleaned_data.get('value')
        process = cleaned_data.get('process')
