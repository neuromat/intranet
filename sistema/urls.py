from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.utils.translation import ugettext_lazy as _

from helpers.views.show_page import display_documents, display_reports, display_add_content

from views import language_change
from activity import views as activity_views
from dissemination import views as dissemination_views
from person import views as person_views
from research import views as research_views
from scientific_mission import views as scientific_views

document_patterns = [
    url(r'^anexo5/$', scientific_views.anexo5, name='anexo5'),
    url(r'^seminar_poster/$', activity_views.seminar_poster, name='seminar_poster'),
]

reports_patterns = [
    url(r'^academic_works/$', research_views.academic_works, name='academic_works'),
    url(r'^articles/$', research_views.articles_report, name='articles'),
    url(r'^dissemination/$', dissemination_views.dissemination_report, name='dissemination_report'),
    url(r'^meetings/$', activity_views.meetings_report, name='meetings_report'),
    url(r'^researchers/$', person_views.researchers, name='researchers_report'),
    url(r'^seminars/$', activity_views.seminars_report, name='seminars_report'),
    url(r'^scientific_mission/$', scientific_views.missions_report, name='missions_report'),
    url(r'^training_programs/$', activity_views.training_programs_report, name='training_programs_report'),
]

content_patterns = [
    url(r'^import_papers/$', research_views.import_papers, name='import_papers'),
    url(r'^citation_names/$', person_views.citation_names, name='citation_names'),
]

urlpatterns = [
    url(r'^', include(admin.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/password_reset/$', auth_views.password_reset, name='admin_password_reset'),
    url(r'^admin/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^language/(?P<language_code>(?:(?:\w{2})|(?:\w{2}\-\w{2})))$', language_change, name='language_change'),
    url(r'^activity/', include('activity.urls')),
    url(r'^research/', include('research.urls')),
    url(r'^dissemination/', include('dissemination.urls')),
    url(r'^scientific_mission/', include('scientific_mission.urls')),
    url(r'^documents/$', display_documents, name='documents'),
    url(r'^documents/', include(document_patterns)),
    url(r'^reports/$', display_reports, name='reports'),
    url(r'^reports/', include(reports_patterns)),
    url(r'^add_content/$', display_add_content, name='add_content'),
    url(r'^add_content/', include(content_patterns)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'suit' not in settings.INSTALLED_APPS:
    admin.site.index_template = 'admin/default_index.html'
    admin.site.app_index_template = 'admin/default_index.html'
    admin.site.index_title = _('Features of the NIRA system')
