from django import forms
from activity.models import TrainingProgram


class TrainingProgramForm(forms.ModelForm):

    class Meta:
        model = TrainingProgram
        fields = ['other_duration']

    class Media:
        js = ('/static/js/activity.js',)