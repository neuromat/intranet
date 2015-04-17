from django.contrib import admin
from research.models import *
from forms import UnpublishedAdminForm
import copy

admin.site.register(TypeAcademicWork)


class UnpublishedAdmin(admin.ModelAdmin):

    fields = ['status', 'title', 'author', 'type', 'paper_status', 'year', 'month', 'key', 'url', 'note']

    list_display = ('authors', 'title', 'type', 'status', 'created')

    list_display_links = ('title',)

    form = UnpublishedAdminForm

admin.site.register(Unpublished, UnpublishedAdmin)


class InProceedingAdmin(admin.ModelAdmin):

    fields = ['title', 'author', 'book_title', 'year', 'month', 'doi', 'editor', 'volume', 'number', 'serie',
              'start_page', 'end_page', 'publisher', 'organization', 'key', 'url', 'note', 'reference']

    list_display = ('authors', 'title', 'created')

    list_display_links = ('title',)

admin.site.register(InProceeding, InProceedingAdmin)


class ArticleAdmin(admin.ModelAdmin):

    fields = ['title', 'author', 'journal', 'year', 'month', 'volume', 'number', 'doi', 'start_page', 'end_page', 'key',
              'url', 'note', 'reference']

    list_display = ('authors', 'title', 'journal', 'created')

    list_display_links = ('title',)

admin.site.register(Article, ArticleAdmin)


class BookAdmin(admin.ModelAdmin):

    fields = ['author', 'title', 'publisher', 'editor', 'year', 'month', 'doi', 'volume', 'serie', 'edition', 'url',
              'key', 'note', 'reference']

    list_display = ('authors', 'title', 'created')

    list_display_links = ('title',)

admin.site.register(Book, BookAdmin)


class InBookAdmin(admin.ModelAdmin):

    fields = ['book', 'chapter', 'start_page', 'end_page']

    list_display = ('book', 'chapter', 'start_page', 'end_page')

    list_display_links = ('book',)

admin.site.register(InBook, InBookAdmin)


class TechReportAdmin(admin.ModelAdmin):

    fields = ['author', 'title', 'institution', 'year', 'month', 'url', 'number', 'type', 'key', 'note', 'reference']

    list_display = ('authors', 'title', 'institution', 'created')

    list_display_links = ('title',)

admin.site.register(TechReport, TechReportAdmin)


class AcademicWorkAdmin(admin.ModelAdmin):

    fields = ['type', 'status', 'title', 'author', 'advisor', 'co_advisor', 'reference']

    list_display = ('title', 'author', 'advisor', 'type', 'status')

    list_display_links = ('title',)

admin.site.register(AcademicWork, AcademicWorkAdmin)


class WorkInProgressAdmin(admin.ModelAdmin):

    fields = ['status', 'description']

    list_display = ('author', 'status', 'description',)

    list_display_links = ('author',)

    # Shows the WorkInProgress according to the user permission
    # Users defined as superuser or NIRA Admin can see all the WorkInProgress
    def get_queryset(self, request):
        qs = super(WorkInProgressAdmin, self).get_queryset(request)
        if request.user.projectmember.is_nira_admin or request.user.is_superuser:
            return qs
        return qs.filter(author=request.user.projectmember)

    # If superuser or NIRA Admin, enable the author field
    def get_fieldsets(self, request, obj=None):
        fieldsets = copy.deepcopy(super(WorkInProgressAdmin, self).get_fieldsets(request, obj))
        if request.user.projectmember.is_nira_admin or request.user.is_superuser:
            fieldsets[0][1]['fields'].insert(0, 'author')
        return fieldsets

    # If not superuser or NIRA Admin, set the author as the current user
    def save_model(self, request, obj, form, change):
        if not request.user.projectmember.is_nira_admin and not request.user.is_superuser:
            if not change:
                obj.author = ProjectMember.objects.get(user=request.user)
        obj.save()

admin.site.register(WorkInProgress, WorkInProgressAdmin)