from django.contrib import admin
from research.models import *
from forms import ArticleAdminForm, BookAdminForm, AuthorsInlineFormset
from django.db.models import Q

admin.site.register(TypeAcademicWork)


class AuthorsInline(admin.TabularInline):
    model = Author
    extra = 1
    formset = AuthorsInlineFormset


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


class SuperResearchResult(admin.ModelAdmin):
    # Shows the research result according to the user permission
    # No restriction for users defined as superuser or NIRA Admin
    def get_queryset(self, request):
        qs = super(SuperResearchResult, self).get_queryset(request)
        if request.user.is_nira_admin or request.user.is_superuser:
            return qs
        return qs.filter(person__user=request.user)


class ArticleAdmin(SuperResearchResult):
    fields = ['team', 'title', 'status', 'type', 'periodical', 'event', 'url', 'hide', 'note']
    list_display = ('team', 'title', 'authors', 'current_status', 'type_of_article')
    list_display_links = ('title',)
    inlines = (AuthorsInline, DraftInline, SubmittedInline, AcceptedInline, PublishedInline, PublishedInPeriodicalInline)
    form = ArticleAdminForm

admin.site.register(Article, ArticleAdmin)


class EventAdmin(admin.ModelAdmin):
    fields = ['name', 'acronym', 'local', 'start_date', 'end_date', 'publisher', 'volume', 'number']
    list_display = ('name', 'local', 'start_date', 'end_date')
    list_display_links = ('name',)

admin.site.register(Event, EventAdmin)


class PeriodicalAdmin(admin.ModelAdmin):
    fields = ['name', 'acronym']
    list_display = ('name',)
    list_display_links = ('name',)

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
    fields = ['type', 'title', 'advisee', 'advisor', 'co_advisor', 'schollarship', 'start_date', 'end_date']
    list_display = ('title', 'advisee', 'advisor', 'type', 'start_date', 'end_date')
    list_display_links = ('title',)

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
