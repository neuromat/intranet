from research import views
from django.conf.urls import url


urlpatterns = [

    url(r'^add_periodicals/$', views.add_periodicals, name='add_periodicals'),
    url(r'^add_papers/$', views.add_papers, name='add_papers'),
    url(r'^periodical_published_papers/$', views.periodical_published_papers, name='periodical_published_papers'),
    url(r'^arxiv_papers/$', views.arxiv_papers, name='arxiv_papers'),
    url(r'^event_papers/$', views.event_papers, name='event_papers'),
    url(r'^update_papers/$', views.update_papers, name='update_papers'),

    # .tex files
    url(r'^articles_tex/$', views.articles_tex, name='articles_tex'),
    url(r'^academic_works_tex/$', views.academic_works_tex, name='academic_works_tex'),

    # .pdf files
    url(r'^academic_works_pdf/$', views.academic_works_pdf, name='academic_works_pdf'),
    url(r'^articles_pdf/$', views.articles_pdf, name='articles_pdf'),

]
