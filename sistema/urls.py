from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.utils.translation import ugettext_lazy as _

from helper_functions.show_page import display_documents
from scientific_mission import views as scientific_views
from activity import views as activity_views

urlpatterns = [
    url(r'^', include(admin.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/password_reset/$', auth_views.password_reset, name='admin_password_reset'),
    url(r'^admin/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^activity/', include('activity.urls')),
    url(r'^research/', include('research.urls')),
    url(r'^person/', include('person.urls')),
    url(r'^dissemination/', include('dissemination.urls')),
    url(r'^scientific_mission/', include('scientific_mission.urls')),
    url(r'^documents/$', display_documents, name='documents'),
    url(r'^documents/anexo5/$', scientific_views.anexo5, name='anexo5'),
    url(r'^documents/seminar_poster/$', activity_views.seminar_poster, name='seminar_poster'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = _('NeuroMat Individual Report of Activities')
admin.site.site_title = _('NIRA admin')
admin.site.index_title = _('Administration')
