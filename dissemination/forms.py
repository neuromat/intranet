from django import forms
from django.forms import TextInput
from dissemination.models import Dissemination


class DisseminationForm(forms.ModelForm):

    class Meta:
        model = Dissemination
        fields = ['link']
        widgets = {
            'link': TextInput(attrs={'size': 55, 'placeholder': 'neuromat.numec.prp.usp.br/example'}),
        }
