from django.contrib import admin
from member.models import *
from django.utils.translation import ugettext_lazy as _
import copy
from forms import *

admin.site.register(Role)
admin.site.register(InstitutionType)


class ProjectMemberAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ['__unicode__', 'role', 'institution']
        }),
        (_('Personal Info'), {
            'fields': ('rg', 'cpf', 'passport')
        }),
        (_('Contact Info'), {
            'fields': ('phone', 'cellphone', 'zipcode', 'street', 'street_complement', 'number', 'district', 'city',
                       'state', 'country')
        }),
    )

    list_display = ('__unicode__', 'role', 'institution')
    list_display_links = ('__unicode__', )

    # Shows the investigators according to the user permission
    def get_queryset(self, request):
        if request.user.projectmember.is_nira_admin or request.user.is_superuser:
            return ProjectMember.objects.all()
        return ProjectMember.objects.filter(user=request.user)

    # If not superuser, do not enable role and institution fields
    # __unicode__ is used to show the name of the user, but it can't be changed here
    def get_readonly_fields(self, request, obj=None):
        ro_fields = super(ProjectMemberAdmin, self).get_readonly_fields(request, obj)
        if request.user.is_superuser:
            ro_fields = list(ro_fields) + ['__unicode__',]
        else:
            ro_fields = list(ro_fields) + ['__unicode__', 'role', 'institution']
        return ro_fields

    # If superuser, display the is_nira_admin and force_password_change fields
    def get_fieldsets(self, request, obj=None):
        fieldsets = copy.deepcopy(super(ProjectMemberAdmin, self).get_fieldsets(request, obj))
        if request.user.is_superuser:
            fieldsets[0][1]['fields'].append('is_nira_admin')
            fieldsets[0][1]['fields'].append('force_password_change')
        return fieldsets

    form = ProjectMemberForm

admin.site.register(ProjectMember, ProjectMemberAdmin)


class OtherAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ['full_name', 'email', 'institution', ]
        }),
        (_('Personal Info'), {
            'fields': ('rg', 'cpf', 'passport')
        }),
        (_('Contact Info'), {
            'fields': ('phone', 'cellphone', 'zipcode', 'street', 'street_complement', 'number', 'district', 'city',
                       'state', 'country')
        }),
    )

    list_display = ('full_name', 'email', 'institution')
    list_display_links = ('full_name', 'email', 'institution')

admin.site.register(Other, OtherAdmin)


class InstitutionAdmin(admin.ModelAdmin):

    fields = ['type', 'name', 'acronym', 'belongs_to']
    list_display = ('type', 'name', 'acronym', 'belongs_to')
    list_display_links = ('name',)

admin.site.register(Institution, InstitutionAdmin)


class BibliographicCitationAdmin(admin.ModelAdmin):
    fields = ['citation_name']
    list_display = ('person_name', 'citation_name')
    list_display_links = ('person_name',)

    # Shows the persons according to the user permission
    def get_queryset(self, request):
        qs = super(BibliographicCitationAdmin, self).get_queryset(request)
        # If super-user, show all
        if request.user.is_superuser:
            return qs
        return qs.filter(person_name=request.user)

    # If superuser, display the person_name field
    def get_fieldsets(self, request, obj=None):
        fieldsets = copy.deepcopy(super(BibliographicCitationAdmin, self).get_fieldsets(request, obj))
        if request.user.is_superuser or request.user.projectmember.is_nira_admin:
            fieldsets[0][1]['fields'].insert(0, 'person_name')
        return fieldsets

    # If not superuser, set the person as the current user
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and not request.user.projectmember.is_nira_admin:
            if not change:
                if BibliographicCitation.person_name.type_of_person == 'm':
                    obj.person_name = ProjectMember.objects.get(user=request.user)
        obj.save()

admin.site.register(BibliographicCitation, BibliographicCitationAdmin)