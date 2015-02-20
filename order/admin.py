from django.contrib import admin
from order.models import *
from forms import *
from django.utils.translation import ugettext_lazy as _
import copy
from django.core.mail import EmailMultiAlternatives
from django.core.mail import BadHeaderError
from django.http import HttpResponse

# Register your models here.


class SuperOrder(admin.ModelAdmin):
    # Shows the requests according to the user permission.
    # Users defined as superuser or NIRA Admin can see all orders
    def get_queryset(self, request):
        qs = super(SuperOrder, self).get_queryset(request)
        if request.user.investigator.is_nira_admin or request.user.is_superuser:
            return qs
        return qs.filter(requester=request.user)

    # If not superuser and not NIRA Admin, do not show the status field
    def get_readonly_fields(self, request, obj=None):
        ro_fields = super(SuperOrder, self).get_readonly_fields(request, obj)
        if not request.user.is_superuser and not request.user.investigator.is_nira_admin:
            ro_fields = list(ro_fields) + ['status']
        return ro_fields

    # If superuser or NIRA Admin, show the requester and protocol fields
    def get_fieldsets(self, request, obj=None):
        fieldsets = copy.deepcopy(super(SuperOrder, self).get_fieldsets(request, obj))
        if request.user.investigator.is_nira_admin or request.user.is_superuser:
            fieldsets[0][1]['fields'].append('requester')
            fieldsets.append((_('Administrative system'), {'fields': ('protocol',)}),)
        return fieldsets

    # If not superuser or NIRA Admin, set the requester as the current user and status as Open
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and not request.user.investigator.is_nira_admin:
            if not change:
                obj.requester = Investigator.objects.get(user=request.user)
                obj.status = 'o'
        obj.save()

        # Check the type of request. It will be used in the email that is sent to the admins of the NIRA.
        type_of_order = obj.type_of_order
        if type_of_order == 'e':
            type_of_order = 'event'
        elif type_of_order == 'h':
            type_of_order = 'hardwaresoftware'
        elif type_of_order == 's':
            type_of_order = 'service'
        elif type_of_order == 't':
            type_of_order = 'ticket'
        elif type_of_order == 'd':
            type_of_order = 'dailystipend'
        else:
            type_of_order = 'reimbursement'

        requester = obj.requester
        id_number = obj.id

        if not change:
            subject, from_email, to = 'NIRA - Novo pedido', 'neuromatematica@gmail.com', 'admin-nira@numec.prp.usp.br'
            text_content = 'Um novo pedido foi gerado no sistema NIRA.'
            html_content = '<p></p><p>O pesquisador %s fez um novo pedido no sistema NIRA. ' \
                           'Clique <a href="http://localhost:8000/admin/order/%s/%s">aqui</a> para ver este pedido</p>'\
                           % (requester, type_of_order, id_number)
            if subject and from_email and to:
                try:
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')

        else:
            subject, from_email, to = 'NIRA - Pedido alterado', 'neuromatematica@gmail.com', 'admin-nira@numec.prp.usp.br'
            text_content = 'Um pedido foi alterado no sistema NIRA.'
            html_content = '<p></p><p>O pesquisador %s alterou o pedido n&uacute;mero %s do NIRA. ' \
                           'Clique <a href="http://localhost:8000/admin/order/%s/%s">aqui</a> para ver este pedido</p>'\
                           % (requester, id_number, type_of_order, id_number)
            if subject and from_email and to:
                try:
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')


class OrderAdmin(SuperOrder):
    list_display = ('id_order', 'date_modified', 'order_date', 'status', 'type_of_order', 'requester')
    list_per_page = 15
    list_filter = ('status', 'type_of_order', 'requester',)

    # Disable the option to add order
    def has_add_permission(self, request, obj=None):
        return False

    # Disable the option to delete order
    def has_delete_permission(self, request, obj=None):
        return False

    # Hide the order link on the main menu
    def get_model_perms(self, request):
        perms = super(OrderAdmin, self).get_model_perms(request)
        perms['list_hide'] = True
        return perms

admin.site.register(Order, OrderAdmin)


class EventAdmin(SuperOrder):
    fieldsets = [
        (None, {
            'fields': ['status']
        }),
        (_('Event Info'), {
            'fields': ('name', 'url', 'value', 'start_date', 'end_date', 'invitation')
        }),
        (_('Purpose'), {
            'fields': ('justification',)
        }),
    ]

    list_display = ('order_number', 'status', 'requester', 'name', 'order_date')

    list_display_links = ('order_number', 'status', 'name', 'order_date')

    form = EventAdminForm

admin.site.register(Event, EventAdmin)


class HardwareSoftwareAdmin(SuperOrder):
    fieldsets = [
        (None, {
            'fields': ['status']
        }),
        (_('Info about the equipment, supplies or miscellaneous'), {
            'fields': ('type', 'quantity', 'url')
        }),
        (_('Purpose'), {
            'fields': ('justification',)
        }),
    ]

    list_display = ('order_number', 'status', 'requester', 'type', 'order_date')

    list_display_links = ('order_number', 'status', 'type', 'order_date')

    form = HardwareSoftwareAdminForm

    # If superuser or NIRA admin, show requester, origin, category and protocol fields.
    def get_fieldsets(self, request, obj=None):
        fieldsets = copy.deepcopy(super(SuperOrder, self).get_fieldsets(request, obj))
        if request.user.investigator.is_nira_admin or request.user.is_superuser:
            fieldsets[0][1]['fields'].append('requester')
            fieldsets[0][1]['fields'].append('origin')
            fieldsets[0][1]['fields'].append('category')
            fieldsets.append((_('Administrative system'), {'fields': ('protocol',)}),)
        return fieldsets

admin.site.register(HardwareSoftware, HardwareSoftwareAdmin)


class ServiceAdmin(SuperOrder):
    fieldsets = [
        (None, {
            'fields': ['status']
        }),
        (_('Service Info'), {
            'fields': ('type',)
        }),
        (_('Purpose'), {
            'fields': ('justification',)
        }),
    ]

    list_display = ('order_number', 'status', 'requester', 'type', 'order_date')

    list_display_links = ('order_number', 'status', 'type', 'order_date')

    form = ServiceAdminForm

    # If superuser or NIRA admin, show requester, origin and protocol fields.
    def get_fieldsets(self, request, obj=None):
        fieldsets = copy.deepcopy(super(SuperOrder, self).get_fieldsets(request, obj))
        if request.user.investigator.is_nira_admin or request.user.is_superuser:
            fieldsets[0][1]['fields'].append('requester')
            fieldsets[0][1]['fields'].append('origin')
            fieldsets.append((_('Administrative system'), {'fields': ('protocol',)}),)
        return fieldsets

admin.site.register(Service, ServiceAdmin)


class TicketAdmin(SuperOrder):
    fieldsets = [
        (None, {
            'fields': ['status']
        }),
        (_('Ticket Info'), {
            'fields': ('type_transportation', 'type', 'origin', 'destination', 'outbound_date',
                       'outbound_date_preference', 'inbound_date', 'inbound_date_preference', 'note')
        }),
        (_('Purpose of the trip'), {
            'fields': ('justification',)
        }),
    ]

    list_display = ('order_number', 'status', 'requester', 'origin', 'destination', 'outbound_date', 'inbound_date',
                    'order_date')

    list_display_links = ('order_number', 'status', 'origin', 'destination', 'outbound_date', 'inbound_date',
                          'order_date')

    form = TicketAdminForm

admin.site.register(Ticket, TicketAdmin)


class DailyStipendAdmin(SuperOrder):
    fieldsets = [
        (None, {
            'fields': ['status']
        }),
        (_('Daily stipend Info'), {
            'fields': ('origin', 'destination', 'departure', 'arrival')
        }),
        (_('Purpose'), {
            'fields': ('justification',)
        }),
    ]

    list_display = ('order_number', 'status', 'requester', 'origin', 'destination', 'order_date')

    list_display_links = ('order_number', 'status', 'origin', 'destination', 'order_date')

admin.site.register(DailyStipend, DailyStipendAdmin)


class ReimbursementAdmin(SuperOrder):
    fieldsets = [
        (None, {
            'fields': ['status']
        }),
        (_('Reimbursement Info'), {
            'fields': ('why',)
        }),
        (_('Purpose'), {
            'fields': ('justification',)
        }),
    ]

    list_display = ('order_number', 'status', 'requester', 'why', 'order_date')

    list_display_links = ('order_number', 'status', 'why', 'order_date')

admin.site.register(Reimbursement, ReimbursementAdmin)