from django.db import models
from django.utils.translation import ugettext_lazy as _
from member.models import Investigator

# Create your models here.


class OrderStatus(models.Model):
    name = models.CharField(_('Name'), max_length=50)

    # Returns the name
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Order status')
        verbose_name_plural = _('Orders status')
        ordering = ('name', )


class Order(models.Model):
    """

    '__unicode__'		Returns the requester.
    'class Meta'		Ordering of data by requester.
    """
    requester = models.ForeignKey(Investigator, verbose_name=_('Investigator'))
    justification = models.TextField(_('Justification'), max_length=500)
    status = models.ForeignKey(OrderStatus, default=1, verbose_name=_('Status'), blank=True, null=True)
    order_date = models.DateTimeField(_('Order date'), auto_now_add=True, blank=True)
    date_modified = models.DateTimeField(_('Modified'), auto_now=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.requester

    # Description of the model / Sort by title
    class Meta:
        ordering = ('requester', )


class Congress(Order):
    """
    An instance of this class is a solicitation for inscription in a congress.

    """
    name = models.CharField(_('Congress name'), max_length=200)
    url = models.URLField(_('URL'), max_length=50, blank=True, null=True)
    value = models.CharField(_('Value'), max_length=15, blank=True, null=True)
    start_date = models.DateField(_('Start date'))
    end_date = models.DateField(_('End date'))
    invitation = models.FileField(_('Invitation'))

    class Meta:
        verbose_name = _('Congress')
        verbose_name_plural = _('Congress')


class HardwareSoftware(Order):
    """
    An instance of this class is a solicitation for a new equipment or a new software.

    """
    type = models.TextField(_('Description'), max_length=500)
    amount = models.IntegerField(_('Amount'), max_length=5)

    class Meta:
        verbose_name = _('Hardware and Software')
        verbose_name_plural = _('Hardwares and Softwares')


class Service(Order):
    """
    An instance of this class is a solicitation for a third party service.

    """
    type = models.TextField(_('Description'), max_length=500)

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')


class Passage(Order):
    """
    An instance of this class is a solicitation for a new passage.

    """
    origin = models.CharField(_('Origin'), max_length=200)
    destination = models.CharField(_('Destination'), max_length=200)
    outbound_date = models.DateField(_('Outbound Date'))
    outbound_date_preference = models.CharField(_('Outbound Preferred time'), max_length=10, blank=True, null=True)
    inbound_date = models.DateField(_('Inbound Date'))
    inbound_date_preference = models.CharField(_('Inbound Preferred time'), max_length=10, blank=True, null=True)
    type = models.NullBooleanField(_('Type of Trip'))
    type_transportation = models.NullBooleanField(_('Type of transportation'))
    note = models.CharField(_('Note'), max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = _('Passage')
        verbose_name_plural = _('Passages')


class DailyStipend(Order):
    """
    An instance of this class is a solicitation for daily stipend.

    """
    origin = models.CharField(_('Origin'), max_length=200)
    destination = models.CharField(_('Destination'), max_length=200)
    departure = models.DateTimeField(_('Departure'))
    arrival = models.DateTimeField(_('Arrival'))

    class Meta:
        verbose_name = _('Daily stipend')
        verbose_name_plural = _('Daily stipends')


class Reimbursement(Order):
    """
    An instance of this class is a reimbursement request.

    """
    why = models.TextField(_('Description'), max_length=500)

    class Meta:
        verbose_name = _('Reimbursement')
        verbose_name_plural = _('Reimbursements')