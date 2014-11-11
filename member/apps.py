# member/apps.py

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MemberConfig(AppConfig):
    name = 'member'
    verbose_name = _('Account')