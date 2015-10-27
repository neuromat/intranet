from django import forms
from models import Article
from django.forms import TextInput


class ArticleAdminForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['url']
        widgets = {
            'url': TextInput(attrs={'size': 90, 'placeholder': 'http://example.com'}),
        }

    class Media:
        js = ('/static/js/research.js',)