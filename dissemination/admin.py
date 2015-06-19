from django.contrib import admin
from dissemination.models import *
from dissemination.forms import *
from django.utils.translation import ugettext_lazy as _

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
    list_display = ('title', 'authors', 'media_outlet', 'date')
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
    list_display = ('title', 'authors', 'media_outlet', 'date')
    list_display_links = ('title', )
    form = DisseminationForm

admin.site.register(External, ExternalAdmin)