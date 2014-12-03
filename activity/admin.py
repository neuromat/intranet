from django.contrib import admin
from activity.models import *
import copy
#from django.utils.translation import ugettext_lazy as _


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
    def get_queryset(self, request):
        qs = super(ActivityAdmin, self).get_queryset(request)
        # If super-user, show all
        if request.user.is_superuser:
            return qs
        return qs.filter(investigator=request.user)

    # If not superuser, do not show the investigator field
    def get_fieldsets(self, request, obj=None):
        fieldsets = copy.deepcopy(super(ActivityAdmin, self).get_fieldsets(request, obj))
        if request.user.is_superuser:
            fieldsets[0][1]['fields'].insert(0, 'investigator')
        return fieldsets

    # If not superuser, set the investigator as the current user
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            if not change:
                obj.investigator = Investigator.objects.get(user=request.user)
        obj.save()


class TrainingProgramAdmin(ActivityAdmin):
    fieldsets = (
        (None, {
            'fields': ['title', 'description', 'date', 'duration']
        }),
    )

    list_display = ('investigator', 'title', 'date', 'duration')
    list_display_links = ('investigator', 'title', 'date', 'duration')

admin.site.register(TrainingProgram, TrainingProgramAdmin)


class SeminarAdmin(ActivityAdmin):
    fieldsets = (
        (None, {
            'fields': ['title', 'date', 'abstract']
        }),
    )

    list_display = ('investigator', 'title', 'date')
    list_display_links = ('investigator', 'title', 'date')

admin.site.register(Seminar, SeminarAdmin)


class ScientificMissionAdmin(ActivityAdmin):
    fieldsets = (
        (None, {
            'fields': ['mission', 'start_date', 'end_date']
        }),
    )

    list_display = ('investigator','mission', 'start_date', 'end_date')
    list_display_links = ('investigator', 'start_date', 'end_date')

admin.site.register(ScientificMission, ScientificMissionAdmin)