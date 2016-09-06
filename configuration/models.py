from django.db import models
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel


class ProcessNumber(SingletonModel):

    process_number = models.CharField(_('Process number'), max_length=255, default='0000-000/00')

    class Meta:
        verbose_name = _('Process number')
        permissions = (("change_process_number", _("Can change the process number.")),)


class CepidName(SingletonModel):

    cepid_name = models.CharField(_('CEPID name'), max_length=255, default='Meu Cepid')

    class Meta:
        verbose_name = _('Cepid name')
        permissions = (("change_cepid_name", _("Can change the Cepid name.")),)


class PosterImage(SingletonModel):

    poster_image = models.ImageField()

    class Meta:
        verbose_name = _('Poster image')
        permissions = (("change_poster_image", _("Can change the poster image.")),)


class QRCode(SingletonModel):

    code_image = models.ImageField()

    class Meta:
        verbose_name = _('QR code')
        permissions = (("change_qr_code", _("Can change the QR code.")),)
