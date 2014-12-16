from django.contrib import admin
from order.models import *
from forms import *
from django.utils.translation import ugettext_lazy as _
import copy
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

# Register your models here.


def nira_admin():
    return User.objects.filter(investigator__is_nira_admin=True)


class SuperOrder(admin.ModelAdmin):
    # Shows the requests according to the user permission. Users defined as NIRA Admin can see all orders
    def get_queryset(self, request):
        qs = super(SuperOrder, self).get_queryset(request)
        if request.user in nira_admin():
            return qs
        return qs.filter(requester=request.user)

    # If not NIRA Admin, do not show the status field
    def get_readonly_fields(self, request, obj=None):
        ro_fields = super(SuperOrder, self).get_readonly_fields(request, obj)
        if request.user not in nira_admin():
            ro_fields = list(ro_fields) + ['status']
        return ro_fields

    # If not NIRA Admin, do not show the requester field
    def get_fieldsets(self, request, obj=None):
        fieldsets = copy.deepcopy(super(SuperOrder, self).get_fieldsets(request, obj))
        if request.user in nira_admin():
            fieldsets[0][1]['fields'].append('requester')
        return fieldsets

    # If not NIRA Admin, set the requester as the current user and status as Open
    def save_model(self, request, obj, form, change):
        if request.user not in nira_admin():
            if not change:
                obj.requester = Investigator.objects.get(user=request.user)
                obj.status = 'o'
        obj.save()

        if not change:
            subject, from_email, to = 'NIRA - Novo pedido', 'neuromatematica@gmail.com', 'admin-nira@numec.prp.usp.br'
            text_content = 'Um novo pedido foi gerado no sistema NIRA.'
            html_content = '<p>Um novo pedido foi gerado no sistema NIRA. ' \
                           '<a href="http://sistema.numec.prp.usp.br/admin/order/order/">Ver pedidos.</a></p>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()


class OrderAdmin(SuperOrder):
    list_display = ('id_order', 'date_modified', 'order_date', 'status', 'type_of_order', 'requester')
    list_per_page = 15
    list_filter = ('status', 'type_of_order', 'requester',)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Order, OrderAdmin)


class EventAdmin(SuperOrder):
    fieldsets = (
        (None, {
            'fields': ['status']
        }),
        (_('Event Info'), {
            'fields': ('name', 'url', 'value', 'start_date', 'end_date', 'invitation')
        }),
        (_('Purpose'), {
            'fields': ('justification',)
        }),
    )

    list_display = ('order_number', 'status', 'requester', 'name', 'order_date')

    list_display_links = ('order_number', 'status', 'name', 'order_date')

admin.site.register(Event, EventAdmin)


class HardwareSoftwareAdmin(SuperOrder):
    fieldsets = (
        (None, {
            'fields': ['status']
        }),
        (_('Hardware or Software Info'), {
            'fields': ('type', 'quantity')
        }),
        (_('Purpose'), {
            'fields': ('justification',)
        }),
    )

    list_display = ('order_number', 'status', 'requester', 'type', 'order_date')

    list_display_links = ('order_number', 'status', 'type', 'order_date')

admin.site.register(HardwareSoftware, HardwareSoftwareAdmin)


class ServiceAdmin(SuperOrder):
    fieldsets = (
        (None, {
            'fields': ['status']
        }),
        (_('Service Info'), {
            'fields': ('type',)
        }),
        (_('Purpose'), {
            'fields': ('justification',)
        }),
    )

    list_display = ('order_number', 'status', 'requester', 'type', 'order_date')

    list_display_links = ('order_number', 'status', 'type', 'order_date')

admin.site.register(Service, ServiceAdmin)


class TicketAdmin(SuperOrder):
    fieldsets = (
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
    )

    list_display = ('order_number', 'status', 'requester', 'origin', 'destination', 'outbound_date', 'inbound_date',
                    'order_date')

    list_display_links = ('order_number', 'status', 'origin', 'destination', 'outbound_date', 'inbound_date',
                          'order_date')

    form = TicketAdminForm

admin.site.register(Ticket, TicketAdmin)


class DailyStipendAdmin(SuperOrder):
    fieldsets = (
        (None, {
            'fields': ['status']
        }),
        (_('Daily stipend Info'), {
            'fields': ('origin', 'destination', 'departure', 'arrival')
        }),
        (_('Purpose'), {
            'fields': ('justification',)
        }),
    )

    list_display = ('order_number', 'status', 'requester', 'origin', 'destination', 'order_date')

    list_display_links = ('order_number', 'status', 'origin', 'destination', 'order_date')

admin.site.register(DailyStipend, DailyStipendAdmin)


class ReimbursementAdmin(SuperOrder):
    fieldsets = (
        (None, {
            'fields': ['status']
        }),
        (_('Reimbursement Info'), {
            'fields': ('why',)
        }),
        (_('Purpose'), {
            'fields': ('justification',)
        }),
    )

    list_display = ('order_number', 'status', 'requester', 'why', 'order_date')

    list_display_links = ('order_number', 'status', 'why', 'order_date')

admin.site.register(Reimbursement, ReimbursementAdmin)