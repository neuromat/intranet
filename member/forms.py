from django import forms
from order.models import Investigator, University
from django.forms import Select
from cep.widgets import CEPInput
from django.utils.translation import ugettext_lazy as _


class InvestigatorForm(forms.ModelForm):

    class Meta:
        model = Investigator

        fields = ['zipcode', 'street', 'district', 'city', 'state', 'country']

        widgets = {
            'zipcode': CEPInput(address={'street': 'id_street', 'district': 'id_district', 'city': 'id_city',
                                         'state': 'id_state'}, attrs={'pattern': '\d{5}-?\d{3}'}),
            'country': Select(attrs={'class': 'bfh-countries', 'data-country': 'BR'}),
            'state': Select(attrs={'class': 'bfh-states', 'data-country': 'id_country'}),
        }

    class Media:
        js = ('/static/bootstrap_form_helpers/dist/js/bootstrap-formhelpers.min.js',)
        css = {
            'all': ('/static/bootstrap_form_helpers/dist/css/bootstrap-formhelpers.min.css',)
        }


class DepartmentForm(forms.ModelForm):
    university = forms.ModelChoiceField(University.objects.all(), label=_('University'),
                                    widget=Select(attrs={'onchange': 'ajax_filter_institutes(this.value);'}))

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs and kwargs['instance'] is not None:
            initial = {'university': kwargs['instance'].institute.university.id}
            if 'initial' in kwargs and kwargs['initial'] is not None:
                kwargs['initial'].update(initial)
            else:
                kwargs['initial'] = initial
        super(DepartmentForm, self).__init__(*args, **kwargs)

    class Media:
        js = ('/static/js/member_department.js',)