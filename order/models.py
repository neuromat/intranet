from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from member.models import Investigator, University, Institute, Department
from django.core.urlresolvers import reverse
from model_utils.managers import InheritanceManager
from django.core.mail import EmailMultiAlternatives
from django.core.mail import BadHeaderError
from django.http import HttpResponse
from django.conf import settings

# Create your models here.

# Defining types of order
EVENT = 'e'
HARDWARE_SOFTWARE = 'h'
SERVICE = 's'
TICKET = 't'
DAILY_STIPEND = 'd'
REIMBURSEMENT = 'r'
ORDER_TYPE = (
    (EVENT, _('Scientific event')),
    (HARDWARE_SOFTWARE, _('Equipment / Supplies / Miscellaneous')),
    (SERVICE, _('Service')),
    (TICKET, _('Ticket')),
    (DAILY_STIPEND, _('Daily stipend')),
    (REIMBURSEMENT, _('Reimbursement')),
)

# Defining status of order
OPEN = 'o'
PENDING = 'p'
CANCELED = 'c'
APPROVED = 'a'
DENIED = 'd'
FINISHED = 'f'
ORDER_STATUS = (
    (OPEN, _('Open')),
    (PENDING, _('Pending')),
    (CANCELED, _('Canceled')),
    (APPROVED, _('Approved')),
    (DENIED, _('Denied')),
    (FINISHED, _('Finished'))
)


class Order(models.Model):
    """

    '__unicode__'		Returns the requester.
    'class Meta'		Ordering of data by date modification.
    'id_order'          Show the IDs as a link to the order.
    'order_number'      Get ID and shows as order number.
    'save'              Send email to the requestor if the order status is changed.
                        Send email to users (NIRA Admin) informing that an order has changed.
                        Send email to users (NIRA Admin) informing that a new order was created.
    """
    requester = models.ForeignKey(Investigator, verbose_name=_('Investigator'))
    justification = models.TextField(_('Justification'), max_length=1000)
    order_date = models.DateTimeField(_('Order date'), auto_now_add=True, blank=True)
    date_modified = models.DateTimeField(_('Modified'), auto_now=True, blank=True)
    type_of_order = models.CharField(_('Type of order'), max_length=1, choices=ORDER_TYPE, blank=True)
    status = models.CharField(max_length=1, default=OPEN, choices=ORDER_STATUS, blank=True)
    protocol = models.IntegerField(_('Protocol'), blank=True, null=True)
    objects = InheritanceManager()

    def __unicode__(self):
        return u'%s' % self.requester

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ('-date_modified', )

    def id_order(self):
        orders = Order.objects.filter(id=self.id).select_subclasses()
        order = orders[0]
        return '<a href="%s">%s</a>' % (reverse('admin:%s_%s_change' % (order._meta.app_label, order._meta.model_name),
                                                args=(order.id,)), order.id)
    id_order.allow_tags = True
    id_order.short_description = _('Order number')
    id_order.admin_order_field = '-id'

    def order_number(self):
        return self.id
    order_number.short_description = _('Order number')
    order_number.admin_order_field = '-id'

    def save(self, *args, **kwargs):
        # Info from settings_local file
        email_host_user = settings.EMAIL_HOST_USER
        nira_admin_email = settings.NIRA_ADMIN_EMAIL
        nira_website = settings.NIRA_WEBSITE
        contact_phone = settings.CONTACT_PHONE
        contact_email = settings.CONTACT_EMAIL

        if self.pk is not None:
            # Info about the order
            check_order = Order.objects.get(pk=self.pk)
            requester_name = check_order.requester
            requester_email = check_order.requester.user.email
            order_type = check_order.type_of_order

            # Check the type of request. It will be used to create the URL in the email that will be sent.
            try:
                if order_type == 'e':
                    order_type = 'event'
                elif order_type == 'h':
                    order_type = 'hardwaresoftware'
                elif order_type == 's':
                    order_type = 'service'
                elif order_type == 't':
                    order_type = 'ticket'
                elif order_type == 'd':
                    order_type = 'dailystipend'
                elif order_type == 'r':
                    order_type = 'reimbursement'
            except NameError:
                return HttpResponse('Invalid order type found.')

            if check_order.status != self.status:
                new_status = self.get_status_display()
                subject = 'NIRA - The status of your order has changed'
                from_email = email_host_user
                to = requester_email
                text_content = 'Hello %s. The status of your order has changed to "%s". See your order by accessing ' \
                               '%s. Please feel free to contact us at %s or %s if you have any questions. ' \
                               'With kind regards, the NIRA team.' \
                               % (requester_name, new_status, nira_website, contact_phone, contact_email)
                html_content = '<p>Hello %s,</p><p>The status of your order has changed to "%s". Click ' \
                               '<a href="%s/admin/order/%s/%s">here</a> to see your request.</p> ' \
                               '<p>Please feel free to contact us at %s or %s if you have any questions.</p> ' \
                               '<p>With kind regards,</p> <p>the NIRA team.</p>' \
                               % (requester_name, new_status, nira_website, order_type, check_order.id, contact_phone,
                                  contact_email)
                if subject and from_email and to:
                    try:
                        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')

            else:
                subject, from_email, to = 'NIRA - Pedido alterado', email_host_user, nira_admin_email
                text_content = 'Um pedido foi alterado no sistema NIRA.'
                html_content = '<p>O(a) pesquisador(a) %s alterou o pedido de n&uacute;mero %s do NIRA. Clique ' \
                               '<a href="%s/admin/order/%s/%s">aqui</a> para ver este pedido.</p>' \
                               % (requester_name, check_order.id, nira_website, order_type, check_order.id)
                if subject and from_email and to:
                    try:
                        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')

        else:
            subject, from_email, to = 'NIRA - Novo pedido', email_host_user, nira_admin_email
            text_content = 'Um novo pedido foi gerado no sistema NIRA.'
            html_content = '<p></p><p>Um novo pedido foi gerado no sistema NIRA. ' \
                           'Clique <a href="%s/admin/order/order">aqui</a> para ver o pedido.</p>' % nira_website
            if subject and from_email and to:
                try:
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')

        super(Order, self).save(*args, **kwargs)


class Event(Order):
    """
    An instance of this class is a solicitation for inscription in an event.

    """
    name = models.CharField(_('Name'), max_length=200)
    url = models.URLField(_('URL'), max_length=50, blank=True, null=True)
    value = models.CharField(_('Value'), max_length=15, blank=True, null=True)
    start_date = models.DateField(_('Start date'))
    end_date = models.DateField(_('End date'))
    invitation = models.FileField(_('Invitation'), blank=True, null=True)

    class Meta:
        verbose_name = _('Scientific event')
        verbose_name_plural = _('Scientific events')

    # Sets the type of order as event.
    def save(self, *args, **kwargs):
        self.type_of_order = EVENT
        super(Event, self).save(*args, **kwargs)


class HardwareSoftware(Order):
    """
    An instance of this class is a purchase request for a new permanent material or a consumable item.

    """
    type = models.TextField(_('Description'), max_length=500)
    quantity = models.IntegerField(_('Quantity'))
    url = models.URLField(_('URL'), max_length=255, blank=True, null=True,
                          help_text='Link to the product details. You may suggest an URL address of the manufacturer of'
                                    ' the product or any store that sells this product.')
    origin = models.CharField(_('Origin'), max_length=1, blank=True, null=True)
    category = models.CharField(_('Category'), max_length=1, blank=True, null=True)
    university = models.ForeignKey(University, verbose_name=_('University'), blank=True, null=True,
                                   help_text='Institution that will receive the equipment, supplies or miscellaneous '
                                             'requested in this order')
    institute = models.ForeignKey(Institute, verbose_name=_('Institute / School / Administrative'),
                                  blank=True, null=True)
    department = models.ForeignKey(Department, verbose_name=_('Department / Research project'), blank=True, null=True)

    class Meta:
        verbose_name = _('Equipment / Supplies / Miscellaneous')
        verbose_name_plural = _('Equipment / Supplies / Miscellaneous')

    # Sets the type of order as equipment / supplies / miscellaneous
    def save(self, *args, **kwargs):
        self.type_of_order = HARDWARE_SOFTWARE
        super(HardwareSoftware, self).save(*args, **kwargs)


class Service(Order):
    """
    An instance of this class is a solicitation for a third party service.

    """
    type = models.TextField(_('Description'), max_length=500)
    origin = models.CharField(_('Origin'), max_length=1, blank=True, null=True)

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    # Sets the type of order as service.
    def save(self, *args, **kwargs):
        self.type_of_order = SERVICE
        super(Service, self).save(*args, **kwargs)


class Ticket(Order):
    """
    An instance of this class is a solicitation for a new ticket.

    """
    origin = models.CharField(_('Origin'), max_length=200)
    destination = models.CharField(_('Destination'), max_length=200)
    outbound_date = models.DateField(_('Outbound Date'))
    outbound_date_preference = models.CharField(_('Outbound Preferred time'), max_length=10, blank=True, null=True)
    inbound_date = models.DateField(_('Inbound Date'), blank=True, null=True)
    inbound_date_preference = models.CharField(_('Inbound Preferred time'), max_length=10, blank=True, null=True)
    type = models.NullBooleanField(_('Type of Trip'))
    type_transportation = models.NullBooleanField(_('Type of transportation'))
    note = models.CharField(_('Note'), max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')

    # Sets the type of order as ticket.
    def save(self, *args, **kwargs):
        self.type_of_order = TICKET
        super(Ticket, self).save(*args, **kwargs)


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

    # Sets the type of order as daily stipend.
    def save(self, *args, **kwargs):
        self.type_of_order = DAILY_STIPEND
        super(DailyStipend, self).save(*args, **kwargs)


class Reimbursement(Order):
    """
    An instance of this class is a reimbursement request.

    """
    why = models.TextField(_('Description'), max_length=500)

    class Meta:
        verbose_name = _('Reimbursement')
        verbose_name_plural = _('Reimbursements')

    # Sets the type of order as reimbursement.
    def save(self, *args, **kwargs):
        self.type_of_order = REIMBURSEMENT
        super(Reimbursement, self).save(*args, **kwargs)