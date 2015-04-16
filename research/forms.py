from django import forms


class UnpublishedAdminForm(forms.ModelForm):

    class Media:
        js = ('/static/js/research_unpublished.js',)
