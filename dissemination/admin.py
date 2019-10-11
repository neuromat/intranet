from django.contrib import admin
from dissemination.models import Topic, InternalMediaOutlet, Internal, ExternalMediaOutlet, External
from dissemination.forms import DisseminationForm

admin.site.register(Topic)
admin.site.register(InternalMediaOutlet)
admin.site.register(ExternalMediaOutlet)


class InternalAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ['title', 'author', 'media_outlet', 'date', 'link', 'topic']
        }),
    )
    filter_horizontal = ('author', 'topic')
    list_display = ('title', 'media_outlet', 'topics', 'date')
    list_display_links = ('title', )
    form = DisseminationForm


admin.site.register(Internal, InternalAdmin)


class ExternalAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ['title', 'author', 'media_outlet', 'date', 'link', 'topic']
        }),
    )
    filter_horizontal = ('author', 'topic')
    list_display = ('title', 'authors', 'media_outlet', 'topics', 'date')
    list_display_links = ('title', )
    form = DisseminationForm


admin.site.register(External, ExternalAdmin)
