from django.contrib import admin
from activity.models import *
from forms import *

admin.site.register(SeminarType)


class MeetingAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ['event_name', 'cepid_event', 'speaker', 'institution', 'description', 'start_date', 'end_date',
                       'url', 'participant']
        }),
    )

    list_display = ('event_name', 'cepid_event', 'start_date', 'end_date')
    list_display_links = ('event_name', )

admin.site.register(Meeting, MeetingAdmin)


class TrainingProgramAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ['meeting', 'speaker', 'title', 'institution', 'description', 'start_date', 'end_date', 'duration',
                       'other_duration']
        }),
    )

    list_display = ('title', 'institution', 'start_date', 'end_date')
    list_display_links = ('title',)
    form = TrainingProgramForm

admin.site.register(TrainingProgram, TrainingProgramAdmin)


class SeminarAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ['meeting', 'category', 'speaker', 'title', 'institution', 'date', 'abstract', 'attachment']
        }),
    )

    list_display = ('category', 'title', 'date')
    list_display_links = ('title',)

admin.site.register(Seminar, SeminarAdmin)