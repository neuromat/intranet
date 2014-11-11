from django.contrib import admin
from member.models import *
from django.utils.translation import ugettext_lazy as _

admin.site.register(Role)
admin.site.register(Institution)


class InvestigatorAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('user', 'nickname', 'role', 'institution',)
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

    # If not superuser, do not show the user combobox
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(InvestigatorAdmin, self).get_readonly_fields(request, obj)
        else:
            return 'user'

admin.site.register(Investigator, InvestigatorAdmin)


class NameCitationAdmin(admin.ModelAdmin):
    fields = ['investigator', 'name']

    list_display = ('investigator', 'name')

    list_display_links = ('investigator',)

admin.site.register(NameCitation, NameCitationAdmin)
