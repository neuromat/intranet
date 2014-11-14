from django import forms
from order.models import Passage
from django.forms import RadioSelect, Select
from django.utils.translation import ugettext_lazy as _


TRIP_ANSWER = (
    ('False', _('Round Trip')),
    ('True', _('One Way')),
)

TRANSPORTATION = (
    ('False', _('Aerial ')),
    ('True', _('Terrestrial')),
)

TIME = (
    ('0', _('-------------------')),
    ('1', _('Morning (6am - 12pm)')),
    ('2', _('Afternoon (12pm - 6pm)')),
    ('3', _('Evening (6pm - 12am)')),
    ('4', _('Night (12am - 6am)')),
)


class PassageAdminForm(forms.ModelForm):

    class Meta:
        model = Passage

        fields = ['type', 'outbound_date_preference', 'inbound_date_preference', 'type_transportation']

        widgets = {
            'type': RadioSelect(choices=TRIP_ANSWER),
            'type_transportation': RadioSelect(choices=TRANSPORTATION),
            'outbound_date_preference': Select(choices=TIME),
            'inbound_date_preference': Select(choices=TIME),
        }

    class Media:
        js = ('/static/js/pedido.js',)
        css = {
            'all': ('/static/css/customization.css',)
        }