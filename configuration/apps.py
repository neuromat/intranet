from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ConfigurationConfig(AppConfig):
    name = 'configuration'
    verbose_name = _('Configuration')
    verbose_name_plural = _('Configurations')
