from django.contrib import admin
from activity.models import *
import copy
from forms import *


class GeneralEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'url')
    list_display_links = ('title', 'start_date', 'end_date', 'url')

admin.site.register(GeneralEvent, GeneralEventAdmin)


class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'url')
    list_display_links = ('title', 'start_date', 'end_date', 'url')

admin.site.register(Meeting, MeetingAdmin)


class ActivityAdmin(admin.ModelAdmin):
    # Shows the activities according to the user permission
    # Users defined as superuser or NIRA Admin can see all activities
    def get_queryset(self, request):
        qs = super(ActivityAdmin, self).get_queryset(request)
        if request.user.investigator.is_nira_admin or request.user.is_superuser:
            return qs
        return qs.filter(investigator=request.user)

    # If superuser or NIRA Admin, enable the investigator field
    def get_fieldsets(self, request, obj=None):
        fieldsets = copy.deepcopy(super(ActivityAdmin, self).get_fieldsets(request, obj))
        if request.user.investigator.is_nira_admin or request.user.is_superuser:
            fieldsets[0][1]['fields'].insert(0, 'investigator')
        return fieldsets

    # If not superuser or NIRA Admin, set the investigator as the current user
    def save_model(self, request, obj, form, change):
        if not request.user.investigator.is_nira_admin or not request.user.is_superuser:
            if not change:
                obj.investigator = Investigator.objects.get(user=request.user)
        obj.save()


class TrainingProgramAdmin(ActivityAdmin):
    fieldsets = (
        (None, {
            'fields': ['title', 'description', 'start_date', 'end_date', 'local', 'duration', 'other_duration']
        }),
    )

    list_display = ('investigator', 'title', 'start_date', 'end_date', 'local', 'duration', 'other_duration')
    list_display_links = ('investigator', 'title', 'start_date', 'end_date', 'local', 'duration', 'other_duration')
    form = TrainingProgramForm

admin.site.register(TrainingProgram, TrainingProgramAdmin)


class SeminarAdmin(ActivityAdmin):
    fieldsets = (
        (None, {
            'fields': ['title', 'date', 'abstract', 'attachment']
        }),
    )

    list_display = ('investigator', 'title', 'date')
    list_display_links = ('investigator', 'title', 'date')

admin.site.register(Seminar, SeminarAdmin)