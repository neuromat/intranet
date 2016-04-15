from django.contrib import admin
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from forms import ArticleAdminForm, BookAdminForm, AcademicWorkAdminForm
from research.models import *


admin.site.register(TypeAcademicWork)


class AuthorsInline(admin.TabularInline):
    model = Author
    extra = 1
    # formset = AuthorsInlineFormset


class DraftInline(admin.StackedInline):
    model = Draft
    extra = 1


class SubmittedInline(admin.StackedInline):
    model = Submitted
    extra = 1


class AcceptedInline(admin.StackedInline):
    model = Accepted
    extra = 1


class PublishedInline(admin.StackedInline):
    model = Published
    extra = 1
    fields = ['doi', 'start_page', 'end_page', 'attachment']


class PublishedInPeriodicalInline(admin.StackedInline):
    model = PublishedInPeriodical
    extra = 1
    fields = ['doi', 'volume', 'number', 'start_page', 'end_page', 'date', 'attachment']


class PeriodicalRISFileInline(admin.StackedInline):
    model = PeriodicalRISFile
    extra = 1
    verbose_name = _('Periodical name')


class EventRISFileInline(admin.StackedInline):
    model = EventRISFile
    extra = 1
    verbose_name = _('Event name')


class SuperResearchResult(admin.ModelAdmin):
    # Shows the research result according to the user permission
    # No restriction for users defined as superuser or NIRA Admin
    def get_queryset(self, request):
        qs = super(SuperResearchResult, self).get_queryset(request)
        if request.user.is_nira_admin or request.user.is_superuser:
            return qs
        return qs.filter(person__user=request.user)


class ArticleAdmin(SuperResearchResult):
    fields = ['team', 'title', 'status', 'type', 'periodical', 'event', 'url', 'ris_file_authors', 'hide', 'note']
    list_display = ('team', 'title', 'authors', 'current_status', 'type_of_article')
    list_display_links = ('title',)
    inlines = (AuthorsInline, DraftInline, SubmittedInline, AcceptedInline, PublishedInline,
               PublishedInPeriodicalInline)
    form = ArticleAdminForm

    # If not superuser or NIRA Admin, the ris_file_authors field becomes read-only.
    def get_readonly_fields(self, request, obj=None):
        ro_fields = super(ArticleAdmin, self).get_readonly_fields(request, obj)
        if not request.user.is_superuser and not request.user.is_nira_admin:
            ro_fields = list(ro_fields) + ['ris_file_authors']
        return ro_fields

admin.site.register(Article, ArticleAdmin)


class EventAdmin(admin.ModelAdmin):
    fields = ['name', 'acronym', 'local', 'start_date', 'end_date', 'publisher', 'volume', 'number']
    list_display = ('name', 'local', 'start_date', 'end_date')
    list_display_links = ('name',)
    inlines = [EventRISFileInline]

admin.site.register(Event, EventAdmin)


class PeriodicalAdmin(admin.ModelAdmin):
    fields = ['name', 'acronym']
    list_display = ('name',)
    list_display_links = ('name',)
    inlines = [PeriodicalRISFileInline]

admin.site.register(Periodical, PeriodicalAdmin)


class BookAdmin(SuperResearchResult):
    fields = ['team', 'type', 'title', 'chapter', 'start_page', 'end_page', 'publisher', 'isbn', 'volume', 'serie',
              'edition', 'doi', 'date', 'url', 'note']
    list_display = ('type', 'authors', 'title', 'date')
    list_display_links = ('title',)
    inlines = (AuthorsInline,)
    form = BookAdminForm

admin.site.register(Book, BookAdmin)


class AcademicWorkAdmin(admin.ModelAdmin):
    fields = ['type', 'title', 'advisee', 'advisor', 'co_advisor', 'funding', 'funding_agency', 'start_date',
              'end_date', 'url', 'abstract']
    list_display = ('title', 'advisee', 'advisor', 'type', 'start_date', 'end_date')
    list_display_links = ('title',)
    form = AcademicWorkAdminForm

    # Shows the academic work according to the user permission
    # No restriction for users defined as superuser or NIRA Admin
    def get_queryset(self, request):
        qs = super(AcademicWorkAdmin, self).get_queryset(request)
        if request.user.is_nira_admin or request.user.is_superuser:
            return qs
        # To see the academic work, the user should be the advisee or the advisor
        return qs.filter(Q(advisee__user=request.user) |
                         Q(advisor__user=request.user) |
                         Q(co_advisor__user=request.user))

    # # Hide journalists in the author or advidor fields
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "author" or db_field.name == "advisor":
    #         kwargs["queryset"] = Person.objects.filter(~Q(role__name='Journalist'))
    #     return super(AcademicWorkAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    #
    # # Hide journalists in the co_advisor field
    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     if db_field.name == "co_advisor":
    #         kwargs["queryset"] = Person.objects.filter(~Q(role__name='Journalist'))
    #     return super(AcademicWorkAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(AcademicWork, AcademicWorkAdmin)
