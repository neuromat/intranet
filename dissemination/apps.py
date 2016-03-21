# dissemination/apps.py

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DisseminationConfig(AppConfig):
    name = 'dissemination'
    verbose_name = _('Dissemination')
    verbose_name_plural = _('Disseminations')