from activity.models import *
from activity.forms import *
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

admin.site.register(SeminarType)


class NewsInline(admin.StackedInline):
    model = News
    extra = 1
    verbose_name = _('Link')
    form = NewsForm


class MeetingAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ['title', 'broad_audience', 'cepid_event', 'local', 'description', 'start_date', 'end_date',
                       'participant']
        }),
    )
    inlines = [NewsInline]
    filter_horizontal = ('participant',)
    list_display = ('title', 'broad_audience', 'cepid_event', 'local', 'start_date', 'end_date')
    list_display_links = ('title', )

admin.site.register(Meeting, MeetingAdmin)


class TrainingProgramAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ['belongs_to',  'speaker', 'title', 'local', 'description', 'number_of_participants',
                       'start_date', 'end_date', 'duration', 'other_duration']
        }),
    )
    inlines = [NewsInline]
    filter_horizontal = ('speaker',)
    list_display = ('speakers', 'title', 'local', 'start_date', 'end_date')
    list_display_links = ('title',)
    form = TrainingProgramForm

    # Shows the Training Programs according to the user permission.
    # Users defined as superuser or NIRA Admin can see all Training Programs.
    def get_queryset(self, request):
        qs = super(TrainingProgramAdmin, self).get_queryset(request)
        if request.user.is_nira_admin or request.user.is_superuser:
            return qs
        return qs.filter(speaker=request.user.projectmember)

admin.site.register(TrainingProgram, TrainingProgramAdmin)


class SeminarAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ['belongs_to', 'category', 'speaker', 'international_guest_lecturer', 'title', 'local', 'room',
                       'date', 'time', 'abstract', 'attachment']
        }),
    )
    inlines = [NewsInline]
    filter_horizontal = ('speaker',)
    list_display = ('category', 'speakers', 'title', 'date')
    list_display_links = ('title',)

    class Media:
        js = ('/static/js/seminar.js',)

admin.site.register(Seminar, SeminarAdmin)
