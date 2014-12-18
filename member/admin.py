from django.contrib import admin
from member.models import *
from django.utils.translation import ugettext_lazy as _
import copy
from forms import *

admin.site.register(Role)
admin.site.register(Institution)


class InvestigatorAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ['user', 'nickname', 'role', 'institution', ]
        }),
        (_('Personal Info'), {
            'fields': ('rg', 'cpf', 'passport')
        }),
        (_('Contact Info'), {
            'fields': ('phone', 'cellphone', 'zipcode', 'street', 'street_complement', 'number', 'district', 'city',
                       'state', 'country')
        }),
    )

    # Shows the investigators according to the user permission
    def get_queryset(self, request):
        if request.user.investigator.is_nira_admin or request.user.is_superuser:
            return Investigator.objects.all()
        return Investigator.objects.filter(user=request.user)

    # If not superuser, do not enable user and role fields
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(InvestigatorAdmin, self).get_readonly_fields(request, obj)
        else:
            return 'user', 'role'

    # If superuser, display the is_nira_admin and force_password_change fields
    def get_fieldsets(self, request, obj=None):
        fieldsets = copy.deepcopy(super(InvestigatorAdmin, self).get_fieldsets(request, obj))
        if request.user.is_superuser:
            fieldsets[0][1]['fields'].append('is_nira_admin')
            fieldsets[0][1]['fields'].append('force_password_change')
        return fieldsets

    form = InvestigatorForm

admin.site.register(Investigator, InvestigatorAdmin)


class BibliographicCitationAdmin(admin.ModelAdmin):
    fields = ['name']

    list_display = ('investigator', 'name')

    list_display_links = ('investigator',)

    # Shows the investigators according to the user permission
    def get_queryset(self, request):
        qs = super(BibliographicCitationAdmin, self).get_queryset(request)
        # If super-user, show all
        if request.user.is_superuser:
            return qs
        return qs.filter(investigator=request.user)

    # If superuser, display the investigator field
    def get_fieldsets(self, request, obj=None):
        fieldsets = copy.deepcopy(super(BibliographicCitationAdmin, self).get_fieldsets(request, obj))
        if request.user.is_superuser:
            fieldsets[0][1]['fields'].insert(0, 'investigator')
        return fieldsets

    # If not superuser, set the investigator as the current user
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            if not change:
                obj.investigator = Investigator.objects.get(user=request.user)
        obj.save()

admin.site.register(BibliographicCitation, BibliographicCitationAdmin)
