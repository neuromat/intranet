from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from .forms import *
from .models import *


admin.site.register(InstitutionType)


class RoleAdmin(TranslationAdmin):
    pass

admin.site.register(Role, RoleAdmin)


class PersonAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ['full_name', 'email', 'role', 'institution']
        }),
        (None, {
            'fields': ('rg', 'cpf', 'passport', 'signature')
        }),
        (_('Contact Info'), {
            'fields': ('phone', 'cellphone', 'zipcode', 'street', 'street_complement', 'number', 'district', 'city',
                       'state', 'country')
        }),
    )
    list_display = ('full_name', 'role', 'institution')
    list_display_links = ('full_name',)
    search_fields = ['full_name', 'role__name']

    # If not superuser or nira_admin, show the current user
    def get_queryset(self, request):
        qs = super(PersonAdmin, self).get_queryset(request)
        if request.user.is_superuser or request.user.is_nira_admin:
            return qs
        return qs.filter(user=request.user)

    # If not superuser or nira_admin, do not enable role and institution fields
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser or request.user.is_nira_admin:
            return super(PersonAdmin, self).get_readonly_fields(request, obj)
        else:
            return 'role', 'institution'

    form = PersonForm

admin.site.register(Person, PersonAdmin)


class InstitutionAdmin(admin.ModelAdmin):
    fields = ['type', 'name', 'acronym', 'belongs_to', 'street', 'street_complement', 'number', 'district', 'city',
              'zipcode']
    list_display = ('type', 'name', 'acronym', 'belongs_to')
    list_display_links = ('name',)

    form = InstitutionForm

admin.site.register(Institution, InstitutionAdmin)


class CitationNameAdmin(admin.ModelAdmin):
    fields = ['person', 'name', 'default_name']
    list_display = ('person', 'name', 'default_name')
    list_display_links = ('name',)

admin.site.register(CitationName, CitationNameAdmin)
