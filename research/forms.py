from django import forms
from models import Article, Book
from django.forms import TextInput, CheckboxSelectMultiple
from django.utils.translation import ugettext_lazy as _

# Papers status
DRAFT = 'd'
SUBMITTED = 's'
ACCEPTED = 'a'
PUBLISHED = 'p'
PAPER_STATUS = (
    (DRAFT, _('Draft')),
    (SUBMITTED, _('Submitted')),
    (ACCEPTED, _('Accepted')),
    (PUBLISHED, _('Published')),
)


class ArticleAdminForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['url', 'status']
        widgets = {
            'url': TextInput(attrs={'size': 90, 'placeholder': 'http://example.com'}),
            'status': CheckboxSelectMultiple(choices=PAPER_STATUS)
        }

    class Media:
        js = ('/static/js/published.js',)
        css = {
            'all': ('/static/css/customization.css',)
        }


class AuthorsInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        """Check that at least one author has been entered."""
        super(AuthorsInlineFormset, self).clean()
        if any(self.errors):
            return
        if not any(cleaned_data and not cleaned_data.get('DELETE', False)
                   for cleaned_data in self.cleaned_data):
            raise forms.ValidationError(_('You must have at least one author'))


class BookAdminForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['type', 'chapter', 'start_page', 'end_page']

    class Media:
        js = ('/static/js/research.js',)
