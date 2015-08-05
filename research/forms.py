from django import forms
from models import Unpublished, Article
from django.forms import TextInput


class UnpublishedAdminForm(forms.ModelForm):

    class Meta:
        model = Unpublished
        fields = ['url']
        widgets = {
            'url': TextInput(attrs={'size': 90, 'placeholder': 'http://example.com'}),
        }

    class Media:
        js = ('/static/js/research.js',)


class ArticleAdminForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['url']
        widgets = {
            'url': TextInput(attrs={'size': 90, 'placeholder': 'http://example.com'}),
        }

    class Media:
        js = ('/static/js/research.js',)