from django.contrib import admin
from order.models import *
from forms import *
from django.utils.translation import ugettext_lazy as _

# Register your models here.

admin.site.register(OrderStatus)


class CongressAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('status', 'requester',)
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

    # Getting the ID and showing as order number
    def order_number(self, obj):
        return obj.congress.id
    order_number.short_description = _('Order number')
    order_number.admin_order_field = '-id'

    # Shows the requests according to the user permission
    def get_queryset(self, request):
        qs = super(CongressAdmin, self).get_queryset(request)
        # If super-user, show all
        if request.user.is_superuser:
            return qs
        return qs.filter(requester=request.user)

    # Auto select current user
    def get_form(self, request, obj=None, **kwargs):
        form = super(CongressAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['requester'].initial = request.user
        return form

    # If not superuser, do not allow user switching
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'requester':
            if not request.user.is_superuser:
                kwargs["queryset"] = Investigator.objects.filter(user=request.user)
        return super(CongressAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    # If not superuser, do not show the status field
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(CongressAdmin, self).get_readonly_fields(request, obj)
        else:
            return 'status'

admin.site.register(Congress, CongressAdmin)


class HardwareSoftwareAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('status', 'requester',)
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

    # Getting the ID and showing as order number
    def order_number(self, obj):
        return obj.hardwaresoftware.id
    order_number.short_description = _('Order number')
    order_number.admin_order_field = '-id'

    # Shows the requests according to the user permission
    def get_queryset(self, request):
        qs = super(HardwareSoftwareAdmin, self).get_queryset(request)
        # If super-user, show all
        if request.user.is_superuser:
            return qs
        return qs.filter(requester=request.user)

    # Auto select current user
    def get_form(self, request, obj=None, **kwargs):
        form = super(HardwareSoftwareAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['requester'].initial = request.user
        return form

    # If not superuser, do not allow user switching
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'requester':
            if not request.user.is_superuser:
                kwargs["queryset"] = Investigator.objects.filter(user=request.user)
        return super(HardwareSoftwareAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    # If not superuser, do not show the status field
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(ReimbursementAdmin, self).get_readonly_fields(request, obj)
        else:
            return 'status'

admin.site.register(HardwareSoftware, HardwareSoftwareAdmin)


class ServiceAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('status', 'requester',)
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

    # Getting the ID and showing as order number
    def order_number(self, obj):
        return obj.service.id
    order_number.short_description = _('Order number')
    order_number.admin_order_field = '-id'

    # Shows the requests according to the user permission
    def get_queryset(self, request):
        qs = super(ServiceAdmin, self).get_queryset(request)
        # If super-user, show all
        if request.user.is_superuser:
            return qs
        return qs.filter(requester=request.user)

    # Auto select current user
    def get_form(self, request, obj=None, **kwargs):
        form = super(ServiceAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['requester'].initial = request.user
        return form

    # If not superuser, do not allow user switching
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'requester':
            if not request.user.is_superuser:
                kwargs["queryset"] = Investigator.objects.filter(user=request.user)
        return super(ServiceAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    # If not superuser, do not show the status field
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(ServiceAdmin, self).get_readonly_fields(request, obj)
        else:
            return 'status'

admin.site.register(Service, ServiceAdmin)


class PassageAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('status', 'requester',)
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

    # Getting the ID and showing as order number
    def order_number(self, obj):
        return obj.passage.id
    order_number.short_description = _('Order number')
    order_number.admin_order_field = '-id'

    # Shows the requests according to the user permission
    def get_queryset(self, request):
        qs = super(PassageAdmin, self).get_queryset(request)
        # If super-user, show all
        if request.user.is_superuser:
            return qs
        return qs.filter(requester=request.user)

    # Auto select current user
    def get_form(self, request, obj=None, **kwargs):
        form = super(PassageAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['requester'].initial = request.user
        return form

    # If not superuser, do not allow user switching
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'requester':
            if not request.user.is_superuser:
                kwargs["queryset"] = Investigator.objects.filter(user=request.user)
        return super(PassageAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    # If not superuser, do not show the status field
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(PassageAdmin, self).get_readonly_fields(request, obj)
        else:
            return 'status'

admin.site.register(Passage, PassageAdmin)


class DailyStipendAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('status', 'requester',)
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

    # Getting the ID and showing as order number
    def order_number(self, obj):
        return obj.dailystipend.id
    order_number.short_description = _('Order number')
    order_number.admin_order_field = '-id'

    # Shows the requests according to the user permission
    def get_queryset(self, request):
        qs = super(DailyStipendAdmin, self).get_queryset(request)
        # If super-user, show all
        if request.user.is_superuser:
            return qs
        return qs.filter(requester=request.user)

    # Auto select current user
    def get_form(self, request, obj=None, **kwargs):
        form = super(DailyStipendAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['requester'].initial = request.user
        return form

    # If not superuser, do not allow user switching
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'requester':
            if not request.user.is_superuser:
                kwargs["queryset"] = Investigator.objects.filter(user=request.user)
        return super(DailyStipendAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    # If not superuser, do not show the status field
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(DailyStipendAdmin, self).get_readonly_fields(request, obj)
        else:
            return 'status'

admin.site.register(DailyStipend, DailyStipendAdmin)


class ReimbursementAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('status', 'requester',)
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

    # Getting the ID and showing as order number
    def order_number(self, obj):
        return obj.reimbursement.id
    order_number.short_description = _('Order number')
    order_number.admin_order_field = '-id'

    # Shows the requests according to the user permission
    def get_queryset(self, request):
        qs = super(ReimbursementAdmin, self).get_queryset(request)
        # If super-user, show all
        if request.user.is_superuser:
            return qs
        return qs.filter(requester=request.user)

    # Auto select current user
    def get_form(self, request, obj=None, **kwargs):
        form = super(ReimbursementAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['requester'].initial = request.user
        return form

    # If not superuser, do not allow user switching
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'requester':
            if not request.user.is_superuser:
                kwargs['queryset'] = Investigator.objects.filter(user=request.user)
        return super(ReimbursementAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    # If not superuser, do not show the status field
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(ReimbursementAdmin, self).get_readonly_fields(request, obj)
        else:
            return 'status'

admin.site.register(Reimbursement, ReimbursementAdmin)