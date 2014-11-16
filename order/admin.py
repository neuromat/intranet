from django.contrib import admin
from order.models import *
from forms import *
from django.utils.translation import ugettext_lazy as _
import copy

# Register your models here.


class SuperOrder(admin.ModelAdmin):
    # Shows the requests according to the user permission
    def get_queryset(self, request):
        qs = super(SuperOrder, self).get_queryset(request)
        # If super-user, show all
        if request.user.is_superuser:
            return qs
        return qs.filter(requester=request.user)

    # If not superuser, do not show the status field
    def get_readonly_fields(self, request, obj=None):
        ro_fields = super(SuperOrder, self).get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            ro_fields = list(ro_fields) + ['status']
        return ro_fields

    # If not superuser, do not show the requester field
    def get_fieldsets(self, request, obj=None):
        fieldsets = copy.deepcopy(super(SuperOrder, self).get_fieldsets(request, obj))
        if request.user.is_superuser:
            fieldsets[0][1]['fields'].append('requester')
        return fieldsets

    # If not superuser, set the requester as the current user and status as Open
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            if not change:
                obj.requester = Investigator.objects.get(user=request.user)
                obj.status = 'o'
        obj.save()

class OrderAdmin(SuperOrder):
    list_display = ('id_order', 'date_modified', 'order_date', 'status', 'type_of_order', 'requester')
    list_per_page = 15
    list_filter = ('status', 'type_of_order', 'requester',)

admin.site.register(Order, OrderAdmin)


class CongressAdmin(SuperOrder):

    fieldsets = (
        (None, {
            'fields': ['status']
        }),
        (_('Congress Info'), {
            'fields': ('name', 'url', 'value', 'start_date', 'end_date', 'invitation')
        }),
        (_('Purpose'), {
            'fields': ('justification',)
        }),
    )

    list_display = ('order_number', 'status', 'requester', 'name', 'order_date')

    list_display_links = ('order_number', 'status', 'name', 'order_date')

admin.site.register(Congress, CongressAdmin)


class HardwareSoftwareAdmin(SuperOrder):

    fieldsets = (
        (None, {
            'fields': ['status']
        }),
        (_('Hardware or Software Info'), {
            'fields': ('type', 'amount')
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


class PassageAdmin(SuperOrder):

    fieldsets = (
        (None, {
            'fields': ['status']
        }),
        (_('Passage Info'), {
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

    form = PassageAdminForm

admin.site.register(Passage, PassageAdmin)


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