# research/apps.py

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ResearchConfig(AppConfig):
    name = 'research'
    verbose_name = _('Research results')
