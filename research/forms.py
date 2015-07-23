from django import forms


class UnpublishedAdminForm(forms.ModelForm):

    class Media:
        js = ('/static/js/research.js',)


class ArticleAdminForm(forms.ModelForm):

    class Media:
        js = ('/static/js/research.js',)