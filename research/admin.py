from django.contrib import admin
from research.models import *


admin.site.register(PaperStatus)
admin.site.register(TypeAcademicWork)

class PaperAdmin(admin.ModelAdmin):

    fields = ['title', 'status', 'author', 'doi', 'issn', 'local', 'volume', 'issue', 'start_page', 'end_page', 'year',
              'url', 'reference']

    list_display = ('title', 'status', 'created', 'modified',)

    list_display_links = ('title', 'status', 'created', 'modified',)

admin.site.register(Paper, PaperAdmin)


class AcademicWorkAdmin(admin.ModelAdmin):

    fields = ['type', 'status', 'title', 'author', 'supervisor', 'co_supervisor', 'reference']

    list_display = ('author', 'type', 'status', 'title',)

    list_display_links = ('author', 'type', 'status', 'title',)

admin.site.register(AcademicWork, AcademicWorkAdmin)


class WorkInProgressAdmin(admin.ModelAdmin):

    fields = ['author', 'status', 'description']

    list_display = ('author', 'status',)

    list_display_links = ('author', 'status',)

admin.site.register(WorkInProgress, WorkInProgressAdmin)
