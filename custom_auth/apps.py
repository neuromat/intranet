from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Custom_AuthConfig(AppConfig):
    name = 'custom_auth'
    verbose_name = _("Authentication")
