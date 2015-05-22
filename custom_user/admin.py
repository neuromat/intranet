from django.contrib import admin
from custom_user.models import *
from django.utils.translation import ugettext_lazy as _
import copy
from forms import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.register(Role)
admin.site.register(InstitutionType)


class PersonAdmin(admin.StackedInline):

    model = Person

    fieldsets = (
        (None, {
            'fields': ['citation_name', 'role', 'institution']
        }),
        (None, {
            'fields': ('rg', 'cpf', 'passport')
        }),
        (_('Contact Info'), {
            'fields': ('phone', 'cellphone', 'zipcode', 'street', 'street_complement', 'number', 'district', 'city',
                       'state', 'country')
        }),
    )

    # If not superuser or nira_admin, do not enable role and institution fields
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser or request.user.person.is_nira_admin:
            return super(PersonAdmin, self).get_readonly_fields(request, obj)
        else:
            return 'role', 'institution'

    # If superuser, display the is_nira_admin and force_password_change fields
    def get_fieldsets(self, request, obj=None):
        fieldsets = copy.deepcopy(super(PersonAdmin, self).get_fieldsets(request, obj))
        if request.user.is_superuser:
            fieldsets[0][1]['fields'].append('is_nira_admin')
            fieldsets[0][1]['fields'].append('force_password_change')
        return fieldsets

    form = PersonForm


class UserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (None, {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
    )

    restricted_fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (None, {'fields': ('first_name', 'last_name', 'email')}),
    )

    inlines = (PersonAdmin, )

    # Shows the members according to the user permission
    def get_queryset(self, request):
        if request.user.person.is_nira_admin or request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(person__user=request.user)

    # If not superuser, show restricted_fieldsets.
    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return super(UserAdmin, self).get_fieldsets(request, obj)
        return self.restricted_fieldsets

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class InstitutionAdmin(admin.ModelAdmin):

    fields = ['type', 'name', 'acronym', 'belongs_to']
    list_display = ('type', 'name', 'acronym', 'belongs_to')
    list_display_links = ('name',)

admin.site.register(Institution, InstitutionAdmin)