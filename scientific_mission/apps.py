# scientific_mission/apps.py

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ScientificMissionConfig(AppConfig):
    name = 'scientific_mission'
    verbose_name = _('Scientific mission')
