from django import forms
from django.forms import TextInput
from activity.models import TrainingProgram, News


class TrainingProgramForm(forms.ModelForm):

    class Meta:
        model = TrainingProgram
        fields = ['other_duration']

    class Media:
        js = ('/static/js/activity.js',)


class NewsForm(forms.ModelForm):

    class Meta:
        model = News
        fields = ['url']
        widgets = {
            'url': TextInput(attrs={'size': 90, 'placeholder': 'http://example.com'}),
        }