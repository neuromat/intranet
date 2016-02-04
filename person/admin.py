from django.contrib import admin
from person.models import *
from django.utils.translation import ugettext_lazy as _
from forms import *

admin.site.register(Role)
admin.site.register(InstitutionType)
admin.site.register(CitationName)


class PersonAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ['full_name', 'email', 'citation_name', 'role', 'institution']
        }),
        (None, {
            'fields': ('rg', 'cpf', 'passport')
        }),
        (_('Contact Info'), {
            'fields': ('phone', 'cellphone', 'zipcode', 'street', 'street_complement', 'number', 'district', 'city',
                       'state', 'country')
        }),
    )
    list_display = ('full_name', 'role', 'institution')
    list_display_links = ('full_name',)

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
    fields = ['type', 'name', 'acronym', 'belongs_to']
    list_display = ('type', 'name', 'acronym', 'belongs_to')
    list_display_links = ('name',)

admin.site.register(Institution, InstitutionAdmin)