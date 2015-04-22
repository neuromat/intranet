from django.contrib import admin
from activity.models import *
from forms import *

admin.site.register(SeminarType)


class MeetingAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ['event_name', 'cepid_event', 'speaker', 'local', 'description', 'start_date', 'end_date',
                       'url', 'participant']
        }),
    )

    list_display = ('event_name', 'cepid_event', 'start_date', 'end_date')
    list_display_links = ('event_name', )

admin.site.register(Meeting, MeetingAdmin)


class TrainingProgramAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ['meeting', 'speaker', 'title', 'local', 'description', 'start_date', 'end_date', 'duration',
                       'other_duration']
        }),
    )

    list_display = ('speakers', 'title', 'local', 'start_date', 'end_date')
    list_display_links = ('title',)
    form = TrainingProgramForm

    # Shows the Training Programs according to the user permission.
    # Users defined as superuser or NIRA Admin can see all Training Programs.
    def get_queryset(self, request):
        qs = super(TrainingProgramAdmin, self).get_queryset(request)
        if request.user.projectmember.is_nira_admin or request.user.is_superuser:
            return qs
        return qs.filter(speaker=request.user.projectmember)

admin.site.register(TrainingProgram, TrainingProgramAdmin)


class SeminarAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ['meeting', 'category', 'speaker', 'title', 'local', 'date', 'abstract', 'attachment']
        }),
    )

    list_display = ('category', 'speakers', 'title', 'date')
    list_display_links = ('title',)

admin.site.register(Seminar, SeminarAdmin)