from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)

admin.site.site_header = _('NeuroMat Individual Report of Activities')
admin.site.site_title = _('NIRA admin')
admin.site.index_title = _('Administration')