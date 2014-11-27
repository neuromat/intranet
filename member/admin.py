from django.contrib import admin
from member.models import *
from django.utils.translation import ugettext_lazy as _

admin.site.register(Role)
admin.site.register(Institution)


class InvestigatorAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('force_password_change', 'user', 'nickname', 'role', 'institution',)
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
        if request.user.is_superuser:
            return Investigator.objects.all()
        return Investigator.objects.filter(user=request.user)

    # If not superuser, do not show force_password_change, user and role fields
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(InvestigatorAdmin, self).get_readonly_fields(request, obj)
        else:
            return 'user', 'force_password_change', 'role'

admin.site.register(Investigator, InvestigatorAdmin)


class BibliographicCitationAdmin(admin.ModelAdmin):
    fields = ['investigator', 'name']

    list_display = ('investigator', 'name')

    list_display_links = ('investigator',)

    # Shows the investigators according to the user permission
    def get_queryset(self, request):
        if request.user.is_superuser:
            return BibliographicCitation.objects.all()
        return BibliographicCitation.objects.filter(investigator=request.user)

    # Auto select current user
    def get_form(self, request, obj=None, **kwargs):
        form = super(BibliographicCitationAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['investigator'].initial = request.user
        return form

    # If not superuser, do not allow user switching
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'investigator':
            if not request.user.is_superuser:
                kwargs["queryset"] = Investigator.objects.filter(user=request.user)
        return super(BibliographicCitationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(BibliographicCitation, BibliographicCitationAdmin)
