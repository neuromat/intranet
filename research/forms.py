from django import forms
from research.models import AcademicWork, WorkInProgress
from django.forms import Select
from django.utils.translation import ugettext_lazy as _

STATUS_ANSWER = (
    ('None', ''),
    ('False', _('In Progress')),
    ('True', _('Concluded')),
)


class AcademicWorkAdminForm(forms.ModelForm):

    class Meta:
        model = AcademicWork

        fields = ['status', 'type', ]

        widgets = {
            'status': Select(choices=STATUS_ANSWER),
        }


class WorkInProgressAdminForm(forms.ModelForm):

    class Meta:
        model = WorkInProgress

        fields = ['status', ]

        widgets = {
            'status': Select(choices=STATUS_ANSWER),
        }