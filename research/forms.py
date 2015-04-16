from django import forms
from research.models import Unpublished
from django.forms import Select, TextInput
from django.utils.translation import ugettext_lazy as _


class UnpublishedAdminForm(forms.ModelForm):

    class Meta:
        model = Unpublished

    class Media:
        js = ('/static/js/research_unpublished.js',)
