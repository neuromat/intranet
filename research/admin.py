from django.contrib import admin
from research.models import *
import copy

admin.site.register(PaperStatus)
admin.site.register(TypeAcademicWork)


class PaperAdmin(admin.ModelAdmin):

    fields = ['title', 'status', 'author', 'doi', 'issn', 'local', 'volume', 'issue', 'start_page', 'end_page', 'year',
              'url', 'reference']

    list_display = ('title', 'status', 'created', 'modified',)

    list_display_links = ('title', 'status', 'created', 'modified',)

admin.site.register(Paper, PaperAdmin)


class AcademicWorkAdmin(admin.ModelAdmin):

    fields = ['type', 'status', 'title', 'author', 'advisor', 'co_advisor', 'reference']

    list_display = ('author', 'type', 'status', 'title',)

    list_display_links = ('author', 'type', 'status', 'title',)

admin.site.register(AcademicWork, AcademicWorkAdmin)


class WorkInProgressAdmin(admin.ModelAdmin):

    fields = ['status', 'description']

    list_display = ('author', 'status', 'description',)

    list_display_links = ('author', 'status', 'description',)

    # Shows the research according to the user permission
    def get_queryset(self, request):
        qs = super(WorkInProgressAdmin, self).get_queryset(request)
        # If super-user, show all
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    # If not superuser, do not show the author field
    def get_fieldsets(self, request, obj=None):
        fieldsets = copy.deepcopy(super(WorkInProgressAdmin, self).get_fieldsets(request, obj))
        if request.user.is_superuser:
            fieldsets[0][1]['fields'].insert(0, 'author')
        return fieldsets

    # If not superuser, set the author as the current user
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            if not change:
                obj.author = Investigator.objects.get(user=request.user)
        obj.save()

admin.site.register(WorkInProgress, WorkInProgressAdmin)
