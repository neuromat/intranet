from django.contrib import admin
from research.models import *
from forms import UnpublishedAdminForm
import copy
from django.db.models import Q

admin.site.register(TypeAcademicWork)


class AuthorsInline(admin.TabularInline):
    model = Author
    extra = 1


class SuperResearchResult(admin.ModelAdmin):
    inlines = (AuthorsInline,)

    # Shows the research result according to the user permission
    # Users defined as superuser or NIRA Admin can see all the research result
    def get_queryset(self, request):
        qs = super(SuperResearchResult, self).get_queryset(request)
        if request.user.is_nira_admin or request.user.is_superuser:
            return qs
        return qs.filter(author=request.user.projectmember)


class UnpublishedAdmin(SuperResearchResult):
    fields = ['status', 'title', 'type', 'paper_status', 'year', 'month', 'key', 'url', 'note']
    list_display = ('authors', 'title', 'type', 'status', 'created')
    list_display_links = ('title',)
    form = UnpublishedAdminForm

admin.site.register(Unpublished, UnpublishedAdmin)


class InProceedingAdmin(SuperResearchResult):
    fields = ['title', 'book_title', 'year', 'month', 'doi', 'editor', 'volume', 'number', 'serie', 'start_page',
              'end_page', 'publisher', 'organization', 'key', 'url', 'note', 'reference']
    list_display = ('authors', 'title', 'created')
    list_display_links = ('title',)

admin.site.register(InProceeding, InProceedingAdmin)


class ArticleAdmin(SuperResearchResult):
    fields = ['title', 'journal', 'year', 'month', 'volume', 'number', 'doi', 'start_page', 'end_page', 'key', 'url',
              'note', 'reference']
    list_display = ('authors', 'title', 'journal', 'created')
    list_display_links = ('title',)

admin.site.register(Article, ArticleAdmin)


class BookAdmin(SuperResearchResult):
    fields = ['title', 'publisher', 'editor', 'year', 'month', 'doi', 'volume', 'serie', 'edition', 'url', 'key',
              'note', 'reference']
    list_display = ('authors', 'title', 'created')
    list_display_links = ('title',)

admin.site.register(Book, BookAdmin)


class InBookAdmin(admin.ModelAdmin):
    fields = ['book', 'chapter', 'start_page', 'end_page']
    list_display = ('book', 'chapter', 'start_page', 'end_page')
    list_display_links = ('book',)

admin.site.register(InBook, InBookAdmin)


class TechReportAdmin(SuperResearchResult):
    fields = ['title', 'institution', 'year', 'month', 'url', 'number', 'type', 'key', 'note', 'reference']
    list_display = ('authors', 'title', 'institution', 'created')
    list_display_links = ('title',)

admin.site.register(TechReport, TechReportAdmin)


class AcademicWorkAdmin(admin.ModelAdmin):
    fields = ['type', 'status', 'title', 'author', 'advisor', 'co_advisor', 'reference']
    list_display = ('title', 'author', 'advisor', 'type', 'status')
    list_display_links = ('title',)

    # Shows the academic work according to the user permission
    # Users defined as superuser or NIRA Admin can see all the academic work
    def get_queryset(self, request):
        qs = super(AcademicWorkAdmin, self).get_queryset(request)
        if request.user.is_nira_admin or request.user.is_superuser:
            return qs
        # To see the academic work, the user should be the author or the advisor
        return qs.filter(Q(author=request.user) | Q(advisor=request.user))

admin.site.register(AcademicWork, AcademicWorkAdmin)


class WorkInProgressAdmin(admin.ModelAdmin):
    fields = ['status', 'description']
    list_display = ('author', 'status', 'description',)
    list_display_links = ('author',)

    # Shows the Work in Progress according to the user permission
    # Users defined as superuser or NIRA Admin can see all
    def get_queryset(self, request):
        qs = super(WorkInProgressAdmin, self).get_queryset(request)
        if request.user.is_nira_admin or request.user.is_superuser:
            return qs
        return qs.filter(author=request.user.projectmember)

    # If superuser or NIRA Admin, enable the author field
    def get_fieldsets(self, request, obj=None):
        fieldsets = copy.deepcopy(super(WorkInProgressAdmin, self).get_fieldsets(request, obj))
        if request.user.is_nira_admin or request.user.is_superuser:
            fieldsets[0][1]['fields'].insert(0, 'author')
        return fieldsets

    # If not superuser or NIRA Admin, set the author as the current user
    def save_model(self, request, obj, form, change):
        if not request.user.is_nira_admin and not request.user.is_superuser:
            if not change:
                obj.author = Person.objects.get(user=request.user)
        obj.save()

admin.site.register(WorkInProgress, WorkInProgressAdmin)