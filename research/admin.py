from django.contrib import admin
from research.models import *
from forms import UnpublishedAdminForm, ArticleAdminForm
from django.db.models import Q

admin.site.register(TypeAcademicWork)
admin.site.register(Journal)


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
    fields = ['team', 'status', 'title', 'type', 'paper_status', 'date', 'url', 'note']
    list_display = ('authors', 'title', 'type', 'status', 'paper_status', 'date')
    list_display_links = ('title',)
    form = UnpublishedAdminForm

admin.site.register(Unpublished, UnpublishedAdmin)


class CommunicationInMeetingAdmin(SuperResearchResult):
    fields = ['team', 'title', 'event', 'doi', 'url', 'note', 'attachment']
    list_display = ('authors', 'title', 'event')
    list_display_links = ('title',)

admin.site.register(CommunicationInMeeting, CommunicationInMeetingAdmin)


class ArticleAdmin(SuperResearchResult):
    fields = ['team', 'title', 'journal', 'status', 'date', 'volume', 'number', 'doi', 'start_page', 'end_page', 'url',
              'note', 'attachment']
    list_display = ('team', 'authors', 'title', 'journal', 'status', 'date')
    list_display_links = ('title',)
    form = ArticleAdminForm

admin.site.register(Article, ArticleAdmin)


class BookAdmin(SuperResearchResult):
    fields = ['team', 'title', 'publisher', 'editor', 'date', 'doi', 'volume', 'serie', 'edition', 'url', 'note']
    list_display = ('authors', 'title', 'date')
    list_display_links = ('title',)

admin.site.register(Book, BookAdmin)


class InBookAdmin(admin.ModelAdmin):
    fields = ['book', 'chapter', 'start_page', 'end_page']
    list_display = ('book', 'chapter', 'start_page', 'end_page')
    list_display_links = ('book',)

admin.site.register(InBook, InBookAdmin)


class EventAdmin(admin.ModelAdmin):
    fields = ['name', 'local', 'start_date', 'end_date']
    list_display = ('name', 'local', 'start_date', 'end_date')
    list_display_links = ('name',)

admin.site.register(Event, EventAdmin)


class AcademicWorkAdmin(admin.ModelAdmin):
    fields = ['type', 'title', 'advisee', 'advisor', 'co_advisor', 'institution', 'schollarship', 'start_date',
              'end_date']
    list_display = ('title', 'advisee', 'advisor', 'type', 'start_date', 'end_date')
    list_display_links = ('title',)

    # Shows the academic work according to the user permission
    # Users defined as superuser or NIRA Admin can see all the academic work
    def get_queryset(self, request):
        qs = super(AcademicWorkAdmin, self).get_queryset(request)
        if request.user.is_nira_admin or request.user.is_superuser:
            return qs
        # To see the academic work, the user should be the author or the advisor
        return qs.filter(Q(author=request.user) | Q(advisor=request.user))

    # Hide journalists in the author or advidor fields
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author" or db_field.name == "advisor":
            kwargs["queryset"] = Person.objects.filter(~Q(role__name='Journalist'))
        return super(AcademicWorkAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    # Hide journalists in the co_advisor field
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "co_advisor":
            kwargs["queryset"] = Person.objects.filter(~Q(role__name='Journalist'))
        return super(AcademicWorkAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(AcademicWork, AcademicWorkAdmin)