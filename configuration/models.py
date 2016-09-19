from django.db import models
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel


class ProcessNumber(SingletonModel):

    process_number = models.CharField(_('Process number'), max_length=255, default='0000/00000-0')

    class Meta:
        verbose_name = _('Process number')
        permissions = (("change_process_number", _("Can change the process number.")),)


class CepidName(SingletonModel):

    cepid_name = models.CharField(_('CEPID name'), max_length=255, default='Meu Cepid')

    class Meta:
        verbose_name = _('Cepid name')
        permissions = (("change_cepid_name", _("Can change the Cepid name.")),)
