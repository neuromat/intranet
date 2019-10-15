# -*- coding: utf-8 -*-
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.admin.sites import AdminSite
from unittest import mock

from helpers.views.date import *

from research.models import AcademicWork, TypeAcademicWork, Person, Article, Draft, Event, Submitted, Accepted, \
                            PublishedInPeriodical, Periodical, Author, ResearchResult, Published
from research.views import scholar, now_plus_five_years, arxiv, import_papers
from research.admin import ArticleAdmin, AcademicWorkAdmin

from custom_auth.models import User


USERNAME = 'myuser'
PASSWORD = 'mypassword'

TEST_FILE = open('./research/citations.ris')

# DRY way for testing


def system_authentication(instance):
    user = User.objects.create_user(username=USERNAME, password=PASSWORD)
    user.is_active = True
    user.is_staff = True
    user.is_superuser = True
    user.save()
    factory = RequestFactory()
    logged = instance.client.login(username=USERNAME, password=PASSWORD)
    return logged, user, factory


def testing_session(instance):

    session = instance.client.session
    session['papers'] = []
    session['periodicals_to_add'] = ['Journal of Statistical Physics',
                                     'Brazilian Journal of Probability and Statistics']
    session['event_papers'] = []
    session['arxiv_papers'] = []
    session['periodical_update_papers'] = []
    session['periodical_published_papers'] = []

    return session


def create_postdoc(type_of_work, title, advisee, advisor, start_date, end_date, abstract):
    postdoc = AcademicWork()
    postdoc.type = type_of_work
    postdoc.title = title
    postdoc.advisee = advisee
    postdoc.advisor = advisor
    postdoc.funding = False
    postdoc.start_date = start_date
    postdoc.end_date = end_date
    postdoc.abstract = abstract
    postdoc.save()
    return postdoc


def create_article(title, team):
    article = Article(title=title, team=team)
    article.save()
    return article


def create_hidden_article(title, team):
    article = Article(title=title, team=team, hide=True)
    article.save()
    return article


def create_draft(article, date):
    draft = Draft(article=article, date=date)
    draft.save()
    return draft


def create_submitted(article, date):
    submitted = Submitted(article=article, date=date)
    submitted.save()
    return submitted


def create_accepted(article, date):
    accepted = Accepted(article=article, date=date)
    article.type = 'p'
    article.save()
    accepted.save()
    return accepted


def create_published_in_periodical(article, date, place_of_publication):
    published = PublishedInPeriodical(article=article, date=date)
    published.save()
    article.periodical = place_of_publication
    article.type = 'p'
    article.save()
    return published


class ResearchTimelineTest(TestCase):
    academic_work = None
    advisee = None
    advisor = None
    abstract = None
    team = None

    place_of_publication = None

    postdoc_01 = None
    postdoc_02 = None
    postdoc_03 = None
    postdoc_04 = None
    postdoc_05 = None
    postdoc_06 = None
    postdoc_07 = None
    postdoc_08 = None

    article_01 = None
    article_02 = None
    article_03 = None
    article_04 = None
    article_05 = None
    article_06 = None
    article_07 = None
    article_08 = None
    article_09 = None

    draft_01 = None
    draft_04 = None
    draft_05 = None
    draft_08 = None
    draft_09 = None

    submitted_01 = None
    submitted_02 = None
    submitted_05 = None

    accepted_01 = None
    accepted_03 = None

    published_01 = None
    published_03 = None
    published_05 = None
    published_04 = None
    published_06 = None
    published_07 = None

    def setUp(self):
        logged, self.user, self.factory = system_authentication(self)
        self.assertEqual(logged, True)

        academic_work = TypeAcademicWork.objects.create(name='Post-doctoral')
        academic_work.save()

        advisee = Person.objects.create(full_name='John Smith')
        advisee.save()

        advisor = Person.objects.create(full_name='Emma Miller')
        advisor.save()

        abstract = 'Mussum ipsum cacilds, vidis litro abertis. Consetis adipiscings elitis. Pra lá , depois divoltis ' \
                   'porris, paradis. Paisis, filhis, espiritis santis.'

        team = "s"

        place_of_publication = Periodical.objects.create(name="Scientific America")
        place_of_publication.save()

        # List of academic works

        # First academic work
        self.postdoc_01 = create_postdoc(academic_work, 'postdoc_01', advisee, advisor, '2018-07-01', '2019-10-19',
                                         abstract)

        # Second academic work
        self.postdoc_02 = create_postdoc(academic_work, 'postdoc_02', advisee, advisor, '2018-07-01', '2019-11-22',
                                         abstract)

        # Third academic work
        self.postdoc_03 = create_postdoc(academic_work, 'postdoc_03', advisee, advisor, '2014-08-05', '2015-06-20',
                                         abstract)

        # Fourth academic work
        self.postdoc_04 = create_postdoc(academic_work, 'postdoc_04', advisee, advisor, '2015-06-25', '2016-01-01',
                                         abstract)

        # Fifth academic work
        self.postdoc_05 = create_postdoc(academic_work, 'postdoc_05', advisee, advisor, '2015-08-26', '2016-01-01',
                                         abstract)

        # Sixth academic work
        self.postdoc_06 = create_postdoc(academic_work, 'postdoc_06', advisee, advisor, '2013-05-20', '2016-01-01',
                                         abstract)

        # Seventh academic work
        self.postdoc_07 = create_postdoc(academic_work, 'postdoc_07', advisee, advisor, '2013-07-01', '2014-07-01',
                                         abstract)

        # Eighth academic work
        self.postdoc_08 = create_postdoc(academic_work, 'postdoc_08', advisee, advisor, '2014-07-01', '2016-01-01',
                                         abstract)

        # List of articles

        # First Article: Draft(20/12/12), Submitted(05/01/14), Accepted(05/01/15), Published(05/11/15)
        self.article_01 = create_article('Artigo 01', team)
        self.article_01.status = [u'd', u's', u'a', u'p']
        self.article_01.save()
        self.draft_01 = create_draft(self.article_01, '2012-12-20')
        self.submitted_01 = create_submitted(self.article_01, '2014-01-05')
        self.accepted_01 = create_accepted(self.article_01, '2015-01-05')
        self.published_01 = create_published_in_periodical(self.article_01, '2015-11-05', place_of_publication)

        # Second Article: Submitted(31/07/14)
        self.article_02 = create_article('Article 02', team)
        self.article_02.status = [u's']
        self.article_02.save()
        self.submitted_02 = create_submitted(self.article_02, '2014-07-31')

        # Third Article: Accepted(31/07/14), Published(05/11/15)
        self.article_03 = create_article('Article 03', team)
        self.article_03.status = [u'a', u'p']
        self.article_03.save()
        self.accepted_03 = create_accepted(self.article_03, '2014-07-31')
        self.published_03 = create_published_in_periodical(self.article_03, '2015-11-15', place_of_publication)

        # Fourth Article: Draft(01/06/14), Published(01/08/15)
        self.article_04 = create_article('Article 04', team)
        self.article_04.status = [u'd', u'p']
        self.article_04.save()
        self.draft_04 = create_draft(self.article_04, '2014-06-01')
        self.published_04 = create_published_in_periodical(self.article_04, '2015-08-01', place_of_publication)

        # Fifth Article: Draft(01/06/14), Published(01/08/15)
        self.article_05 = create_article('Article 05', team)
        self.article_05.status = [u'd', u'p']
        self.article_05.save()
        self.draft_05 = create_draft(self.article_05, '2014-06-01')
        self.published_05 = create_published_in_periodical(self.article_05, '2015-08-01', place_of_publication)

        # Sixth Article: Published(30/06/14)
        self.article_06 = create_article('Article 06', team)
        self.article_06.status = [u'p']
        self.article_06.save()
        self.published_06 = create_published_in_periodical(self.article_06, '2014-06-30', place_of_publication)

        # Seventh Article: Published(01/07/14)
        self.article_07 = create_article('Article 07', team)
        self.article_07.status = [u'p']
        self.article_07.save()
        self.published_07 = create_published_in_periodical(self.article_07, '2014-07-01', place_of_publication)

        # Eighth Article: Draft(30/06/14)
        self.article_08 = create_article('Article 08', team)
        self.article_08.status = [u'd']
        self.article_08.save()
        self.draft_08 = create_draft(self.article_08, '2014-06-30')

        # Nineth Article: Draft(30/06/14)
        self.article_09 = create_hidden_article('Article 09', team)
        self.article_09.status = [u'd']
        self.article_09.save()
        self.draft_09 = create_draft(self.article_09, '2014-06-30')

    def test_current_academic_works_report(self):
        """ Report of current academic works is fine """
        start_date = '01/07/2018'
        end_date = '19/09/2019'

        response = self.client.post(reverse('academic_works'), {'start_date': start_date, 'end_date': end_date})

        titles = []
        concluded_count = 0

        for lista in response.context['data']['list']:
            if not lista['concluded']:
                concluded_count += 1

            for item in lista['data']:
                titles.append(item.title)

        self.assertEqual(len(response.context['data']['list']), 2)
        self.assertEqual(concluded_count, 2)
        self.assertTrue(self.postdoc_01.title in titles)
        self.assertTrue(self.postdoc_02.title in titles)

    def test_previous_academic_works_report(self):
        """ Report of previous academic works is fine """
        start_date = '01/01/2013'
        end_date = '01/01/2019'

        response = self.client.post(reverse('academic_works'), {'start_date': start_date, 'end_date': end_date})

        titles = []
        concluded_count = 0

        for lista in response.context['data']['list']:
            if not lista['concluded']:
                concluded_count += 1

            for item in lista['data']:
                titles.append(item.title)

        self.assertEqual(len(response.context['data']['list']), 8)
        self.assertEqual(concluded_count, 2)
        self.assertTrue(self.postdoc_01.title in titles)
        self.assertTrue(self.postdoc_02.title in titles)
        self.assertTrue(self.postdoc_03.title in titles)
        self.assertTrue(self.postdoc_04.title in titles)
        self.assertTrue(self.postdoc_05.title in titles)
        self.assertTrue(self.postdoc_06.title in titles)
        self.assertTrue(self.postdoc_08.title in titles)

    def test_current_articles_report(self):

        """ Report of current articles is fine """
        start_date = '01/07/2014'
        end_date = '31/07/2015'

        response = self.client.post(reverse('articles'), {'start_date': start_date, 'end_date': end_date})

        self.assertEqual(len(response.context['draft_or_submitted']), 5)
        self.assertEqual(len(response.context['published_or_accepted']), 3)

        accepted_articles = []
        drafted_articles = []
        hide_drafted_articles = []
        published_articles = []
        submitted_articles = []
        show_drafted_articles = []

        for item in response.context['draft_or_submitted']:

            if item.article.hide:
                hide_drafted_articles.append(item.article.title)
            else:
                show_drafted_articles.append(item.article.title)

            if u's' in item.article.status:
                submitted_articles.append(item)
            if u'd' in item.article.status:
                drafted_articles.append(item)

        for item in response.context['published_or_accepted']:

            if u'p' in item.article.status:
                published_articles.append(item)
            if u'a' in item.article.status:
                accepted_articles.append(item)

        for item in response.context['draft_or_submitted']:
            if item.article.hide:
                hide_drafted_articles.append(item.article.title)
            else:
                show_drafted_articles.append(item.article.title)

        #  Testing hidden articles
        self.assertTrue(self.article_04.title in show_drafted_articles)
        self.assertTrue(self.article_05.title in show_drafted_articles)
        self.assertTrue(self.article_08.title in show_drafted_articles)
        self.assertTrue(self.article_09.title in hide_drafted_articles)

        #  Testing submitted
        submitted_titles = [item.article.title for item in submitted_articles]
        self.assertTrue(self.article_02.title in submitted_titles)

        #  Testing accepted
        accepted_titles = [item.article.title for item in accepted_articles]
        self.assertTrue(self.article_01.title in accepted_titles)
        self.assertTrue(self.article_03.title in accepted_titles)

        #  Testing published
        published_titles = [item.article.title for item in published_articles]
        self.assertTrue(self.article_07.title in published_titles)

    def test_articles_report_get_request(self):

        response = self.client.get(reverse('articles'))
        self.assertTemplateUsed(response, 'report/research/articles.html')

    def test_articles_report_with_end_date_sooner_than_start_date_raises_error_message(self):
        start_date = '01/07/2014'
        end_date = '31/07/2013'

        response = self.client.post(reverse('articles'), {'start_date': start_date, 'end_date': end_date})
        for message in response.context['messages']:
            self.assertEqual(message.message, _('You entered a wrong date format or the end date is not greater '
                                                'than or equal to the start date.'))

    def test_articles_report_with_appropriate_dates_uses_articles_report_html_template(self):
        start_date = '01/07/2013'
        end_date = '31/07/2014'

        response = self.client.post(reverse('articles'), {'start_date': start_date, 'end_date': end_date})
        self.assertTemplateUsed(response, 'report/research/articles_report.html')

    def test_articles_report_with_empty_start_date_returns_1970_january_first_as_initial_date(self):
        start_date = ''
        end_date = '31/07/2014'

        response = self.client.post(reverse('articles'), {'start_date': start_date, 'end_date': end_date})
        self.assertTrue(b'start_date=1970-01-01' in response.content)

    def test_articles_report_with_empty_start_date_returns_today_plus_30_days_as_end_date(self):
        start_date = '01/07/2013'
        end_date = ''
        today_plus_30 = now_plus_thirty().strftime('%Y-%m-%d')

        response = self.client.post(reverse('articles'), {'start_date': start_date, 'end_date': end_date})
        self.assertTrue('end_date='+today_plus_30 in str(response.content))

    def test_articles_report_with_wrong_date_format_raises_error_message(self):
        start_date = '2013/27/01'
        end_date = '2014/31/07'

        response = self.client.post(reverse('articles'), {'start_date': start_date, 'end_date': end_date})
        for message in response.context['messages']:
            self.assertEqual(message.message, _('You entered a wrong date format or the end date is not greater '
                                                'than or equal to the start date.'))

    def test_articles_file_uses_articles_html_when_passing_tex_as_extension(self):
        date_departure1 = timezone.now() - timezone.timedelta(367)
        date_arrival1 = timezone.now() + timezone.timedelta(1)

        response = self.client.get(
            reverse('articles_file'),
            {'start_date': date_departure1.date().strftime("%Y-%m-%d"),
             'end_date': date_arrival1.date().strftime("%Y-%m-%d"),
             'extension': '.tex'})

        self.assertTemplateUsed(response, 'report/research/tex/articles.tex')

    def test_missions_file_text_renders_pdf_when_not_passing_tex_as_extension(self):
        date_departure1 = timezone.now() - timezone.timedelta(367)
        date_arrival1 = timezone.now() + timezone.timedelta(1)

        response = self.client.get(
            reverse('articles_file'),
            {'start_date': date_departure1.date().strftime("%Y-%m-%d"),
             'end_date': date_arrival1.date().strftime("%Y-%m-%d"),
             'extension': '.doc'})

        self.assertTemplateUsed(response, 'report/research/pdf/articles.html')
        self.assertTrue('b\'%PDF' in str(response.content))

    def test_academic_works_get_request(self):

        response = self.client.get(reverse('academic_works'))
        self.assertTemplateUsed(response, 'report/research/academic_works.html')

    def test_academics_works_with_end_date_sooner_than_start_date_raises_error_message(self):
        start_date = '01/07/2014'
        end_date = '31/07/2013'

        response = self.client.post(reverse('academic_works'), {'start_date': start_date, 'end_date': end_date})
        for message in response.context['messages']:
            self.assertEqual(message.message, _('You entered a wrong date format or the end date is not greater '
                                                'than or equal to the start date.'))

    def test_academics_works_with_appropriate_dates_uses_academic_works_report_html_template(self):
        start_date = '01/07/2013'
        end_date = '31/07/2014'

        response = self.client.post(reverse('academic_works'), {'start_date': start_date, 'end_date': end_date})
        self.assertTemplateUsed(response, 'report/research/academic_works_report.html')

    def test_academics_works_with_empty_start_date_returns_all_projects_from_1970_january_first(self):
        start_date = ''
        end_date = '31/07/2014'

        oldest_academic_works_start_date = \
            AcademicWork.objects.all().order_by('start_date')[0].start_date.strftime("%b %d, %Y")

        response = self.client.post(reverse('academic_works'), {'start_date': start_date, 'end_date': end_date})
        self.assertTrue(oldest_academic_works_start_date in str(response.content))

    def test_academics_works_with_empty_start_date_returns_1970_january_first_as_initial_date(self):
        start_date = '31/06/2014'
        end_date = '31/07/2014'

        oldest_academic_works_start_date = \
            AcademicWork.objects.all().order_by('start_date')[0].start_date.strftime("%b %d, %Y")

        response = self.client.post(reverse('academic_works'), {'start_date': start_date, 'end_date': end_date})
        self.assertFalse(oldest_academic_works_start_date in str(response.content))

    def test_academics_works_with_empty_start_date_returns_today_plus_30_days_as_end_date(self):
        start_date = '01/07/2013'
        end_date = ''

        newest_academic_works_end_date = \
            AcademicWork.objects.all().order_by('-end_date')[0].end_date.strftime("%b. %d, %Y")

        response = self.client.post(reverse('academic_works'), {'start_date': start_date, 'end_date': end_date})
        self.assertTrue(newest_academic_works_end_date in str(response.content))

    def test_academics_works_with_wrong_date_format_raises_error_message(self):
        start_date = '2013/27/01'
        end_date = '2014/31/07'

        response = self.client.post(reverse('academic_works'), {'start_date': start_date, 'end_date': end_date})
        for message in response.context['messages']:
            self.assertEqual(message.message, _('You entered a wrong date format or the end date is not greater '
                                                'than or equal to the start date.'))

    def test_academics_works_file_uses_articles_html_when_passing_tex_as_extension(self):
        date_departure1 = timezone.now() - timezone.timedelta(367)
        date_arrival1 = timezone.now() + timezone.timedelta(1)

        response = self.client.get(
            reverse('academic_works_file'),
            {'start_date': date_departure1.date().strftime("%Y-%m-%d"),
             'end_date': date_arrival1.date().strftime("%Y-%m-%d"),
             'extension': '.tex'})

        self.assertTemplateUsed(response, 'report/research/tex/academic_works.tex')

    def test_academics_works_file_text_renders_pdf_when_not_passing_tex_as_extension(self):
        date_departure1 = timezone.now() - timezone.timedelta(367)
        date_arrival1 = timezone.now() + timezone.timedelta(1)

        response = self.client.get(
            reverse('academic_works_file'),
            {'start_date': date_departure1.date().strftime("%Y-%m-%d"),
             'end_date': date_arrival1.date().strftime("%Y-%m-%d"),
             'extension': '.doc'})

        self.assertTemplateUsed(response, 'report/research/pdf/academic_works.html')
        self.assertTrue('b\'%PDF' in str(response.content))

    def test_previous_articles_report(self):
        """ Report of previous articles is fine """
        start_date = '01/07/2013'
        end_date = '31/07/2014'

        response = self.client.post(reverse('articles'), {'start_date': start_date, 'end_date': end_date})

        self.assertEqual(len(response.context['draft_or_submitted']), 6)
        self.assertEqual(len(response.context['published_or_accepted']), 3)

        accepted_articles = []
        drafted_articles = []
        hide_drafted_articles = []
        published_articles = []
        submitted_articles = []
        show_drafted_articles = []

        for item in response.context['draft_or_submitted']:

            if item.article.hide:
                hide_drafted_articles.append(item.article.title)
            else:
                show_drafted_articles.append(item.article.title)

            if u's' in item.article.status:
                submitted_articles.append(item)
            if u'd' in item.article.status:
                drafted_articles.append(item)

        for item in response.context['published_or_accepted']:

            if u'p' in item.article.status:
                published_articles.append(item)
            if u'a' in item.article.status:
                accepted_articles.append(item)

        for item in response.context['draft_or_submitted']:
            if item.article.hide:
                hide_drafted_articles.append(item.article.title)
            else:
                show_drafted_articles.append(item.article.title)

        self.assertTrue(self.article_04.title in show_drafted_articles)
        self.assertTrue(self.article_05.title in show_drafted_articles)
        self.assertTrue(self.article_08.title in show_drafted_articles)
        self.assertTrue(self.article_09.title in hide_drafted_articles)

        submitted_titles = [item.article.title for item in submitted_articles]
        self.assertTrue(self.article_01.title in submitted_titles)
        self.assertTrue(self.article_02.title in submitted_titles)

        accepted_titles = [item.article.title for item in accepted_articles]
        self.assertTrue(self.article_03.title in accepted_titles)

        published_titles = [item.article.title for item in published_articles]
        self.assertTrue(self.article_06.title in published_titles)
        self.assertTrue(self.article_07.title in published_titles)


class ScholarTest(TestCase):
    """
    Methods that get data from google scholar
    """
    papers_list = []
    specific_paper_title = ''
    specific_paper_date = ''
    wrong_paper_title = ''
    wrong_paper_date = ''
    valid_scholar_list = []
    valid_scholar = False

    def setUp(self):
        self.papers_list = [
            {
                'Hydrodynamic limit for interacting neurons':
                    '/citations?view_op=view_citation&amp;hl=pt-BR&amp;oe=ASCII&amp;user=OaY57UIAAAAJ&amp;pagesize=100'
                    '&amp;citation_forview=OaY57UIAAAAJ:u-x6o8ySG0sC'},
            {
                'The solution of the complete nontrivial cycle intersection problem for permutations':
                    '/citations?view_op=view_citation&amp;hl=pt-BR&amp;oe=ASCII&amp;user=OaY57UIAAAAJ&amp;pagesize=100'
                    '&amp;citation_for_view=OaY57UIAAAAJ:J_g5lzvAfSwC'},
            {
                'Infinite systems of interacting chains with memory of variable length—a stochastic model for '
                'biological neural nets':
                    '/citations?view_op=view_citation&amp;hl=pt-BR&amp;oe=ASCII&amp;user=OaY57UIAAAAJ&amp;pagesize'
                    '=100&amp;citation_for_view=OaY57UIAAAAJ:u5HHmVD_uO8C'}]
        self.specific_paper_title = 'Hydrodynamic limit for interacting neurons'
        self.specific_paper_date = datetime.date(2015, 2, 1)
        self.specific_paper_link = 'http://link.springer.com/article/10.1007/s10955-014-1145-1'
        self.wrong_paper_title = 'Hydrodynamics limits for interactings neuron'
        self.wrong_paper_date = datetime.date(2010, 1, 15)

    def test_get_papers(self):
        """
        Are we taking the papers successfully?
        Well, if we find our little list in the list from Scholar, the function is working fine
        i.e. Google hasn't changed the names of the classes from Scholar.
        """
        ret = False
        scholar_list = scholar()
        scholar_titles = []

        for paper in scholar_list:
            scholar_titles.append(list(paper.keys())[0])

        for paper in self.papers_list:
            if list(paper.keys())[0] in scholar_titles:
                ret = True
            else:
                ret = False

        self.valid_scholar_list.extend(scholar_list)
        self.assertTrue(ret)

    # def test_get_paper_info(self):
    #     """
    #     Are we getting the paper date and url successfully?
    #     Obs: this test depends on test_get_papers
    #     """
    #     scholar_list = scholar()
    #     result = scholar_info(scholar_list, self.specific_paper_title)
    #     self.assertEqual(result[0], self.specific_paper_date)
    #     self.assertEqual(result[1], self.specific_paper_link)
    #     self.assertNotEqual(result[0], self.wrong_paper_date)
    #     self.assertNotEqual(result[1], self.wrong_paper_date)


class DateTest(TestCase):
    """
    Testing methods that handle dates
    """

    def test_now_plus_five_years(self):
        """
        Test if helper method works
        """

        date = datetime.datetime.now() + datetime.timedelta(days=5*365)
        date = date.strftime("%Y%m%d %H:%M:%S")
        date = datetime.datetime.strptime(date, '%Y%m%d %H:%M:%S').date()
        npfy = now_plus_five_years()
        self.assertEqual(npfy, date)


class ArticlesTest(TestCase):
    """
    Testing things about the Articles model
    """

    def setUp(self):
        logged, self.user, self.factory = system_authentication(self)
        self.assertEqual(logged, True)

        title = "Test article"
        team = "Test team"
        self.published = Article(title=title, team=team, status='Published')
        self.accepted = Article(title=title, team=team, status='Accepted')
        self.submitted = Article(title=title, team=team, status='Submitted')
        self.draft = Article(title=title, team=team, status='Draft')

    def current_status_test(self):
        self.assertEqual('Published', self.published.current_status())
        self.assertEqual('Accepted', self.accepted.current_status())
        self.assertEqual('Submitted', self.submitted.current_status())
        self.assertEqual('Draft', self.draft.current_status())
        self.assertNotEqual('Published', self.accepted.current_status())

    def test_get_request_redirects_to_import_papers(self):
        response = self.client.get(reverse('add_periodicals'), follow=True)
        self.assertRedirects(response, reverse('import_papers'), 302)


class ArXivTest(TestCase):
    """ Test method for ArXiv handler. This should work if arxiv doesn't change it's classes """
    def setUp(self):
        self.arxiv_url = 'http://arxiv.org/abs/1601.03704'
        self.date = datetime.date(2016, 1, 14)
        self.wrong_date = datetime.date(2015, 1, 14)

    def test_arxiv(self):
        date = arxiv(self.arxiv_url)
        self.assertEqual(self.date, date)
        self.assertNotEqual(self.wrong_date, date)


class ImportPaperTest(TestCase):

    def setUp(self):
        logged, self.user, self.factory = system_authentication(self)
        self.assertEqual(logged, True)

    def test_import_file(self):

        response = self.client.get(reverse('import_papers'))
        self.assertEqual(response.status_code, 200)

        # Testing import_papers using an example of .ris
        req = RequestFactory()
        request = req.post(reverse('import_papers'), {'file': TEST_FILE})
        request.user = self.user
        request.session = {}
        request.resolver_match = mock.Mock()
        request.resolver_match.url_name = "import_papers"
        response = import_papers(request)
        self.assertEqual(response.status_code, 200)

        not_ris_file = SimpleUploadedFile('citations.jpg', b'rb', content_type='image/jpeg')
        response = self.client.post(reverse('import_papers'), {'file': not_ris_file})
        self.assertEqual(response.status_code, 200)


class AddPeriodicalsTest(TestCase):

    def setUp(self):
        logged, self.user, self.factory = system_authentication(self)
        self.assertEqual(logged, True)

    def test_add_periodicals(self):

        # Redirect status
        response = self.client.post(reverse('add_periodicals'), {'action': 'back'})
        self.assertEqual(response.status_code, 302)


class AddPapersTest(TestCase):

    def setUp(self):

        logged, self.user, self.factory = system_authentication(self)
        self.assertEqual(logged, True)

        session = testing_session(self)
        session.save()

    def test_add_papers(self):

        response = self.client.post(reverse('add_papers'), {'action': 'back'})
        self.assertEqual(response.status_code, 200)


class PeriodicalPublishedTest(TestCase):

    def setUp(self):
        logged, self.user, self.factory = system_authentication(self)
        self.assertEqual(logged, True)

        session = testing_session(self)
        session.save()

    def test_periodical_published_papers(self):

        response = self.client.post(reverse('periodical_published_papers'), {'action': 'next'})
        self.assertEqual(response.status_code, 200)


class ArxivPapersTest(TestCase):

    def setUp(self):
        logged, self.user, self.factory = system_authentication(self)
        self.assertEqual(logged, True)

        session = testing_session(self)
        session.save()

    def test_arxiv_papers(self):

        response = self.client.post(reverse('arxiv_papers'), {'action': 'add'})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('arxiv_papers'), {'action': 'next'})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('arxiv_papers'), {'action': 'back'})
        self.assertEqual(response.status_code, 200)


class EventPapersTest(TestCase):

    def setUp(self):
        self.title = 'Identifying interacting pairs of sites'
        Article.objects.create(team='s', title=self.title, research_result_type='a')

        self.paper, created = Event.objects.get_or_create(
            name='Event test',
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(1),
            local='São Paulo')

        paper_id = self.paper.id

        researcher1 = Person.objects.create(full_name='Galves, A')
        researcher2 = Person.objects.create(full_name='Orlandi, E')
        researcher3 = Person.objects.create(full_name='Takahashi, DY')

        self.authors = [researcher1, researcher2, researcher3]

        self.data = {'paper_id': str(paper_id),
                     'paper_team_' + str(paper_id): ['s'],
                     'paper_title_' + str(paper_id): [self.title],
                     'paper_author_' + str(paper_id): self.authors,
                     'paper_event_' + str(paper_id): paper_id,
                     'paper_start_page_' + str(paper_id): ['443'],
                     'paper_end_page_' + str(paper_id): ['459'],
                     'paper_date_' + str(paper_id): ['2015-01-06']}

    def test_event_papers2(self):

        session = self.client.session
        session['event_papers'] = []
        session['arxiv_papers'] = []
        session['periodical_update_papers'] = []
        session.save()

        response = self.client.post(reverse('event_papers'), {'action': 'next'})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('event_papers'), {'action': 'back'})
        self.assertEqual(response.status_code, 200)

    def test_event_papers_get_request_redirects_to_import_papers(self):
        response = self.client.get(reverse('event_papers'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('import_papers'))

    def test_event_papers_invalid_post_request_redirects_to_import_papers(self):
        response = self.client.post(reverse('event_papers'), {'action': 'addnextback'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('import_papers'))

    def test_event_papers_post_request_with_next_action_renders_periodical_update_papers_html(self):
        session = self.client.session
        session['periodical_update_papers'] = []
        session.save()

        response = self.client.post(reverse('event_papers'), {'action': 'next'})
        self.assertTemplateUsed(response, 'report/research/periodical_update_papers.html')

    def test_event_papers_post_request_with_back_action_renders_arxiv_papers_html(self):
        session = self.client.session
        session['arxiv_papers'] = []
        session.save()

        response = self.client.post(reverse('event_papers'), {'action': 'back'})
        self.assertTemplateUsed(response, 'report/research/arxiv_papers.html')

    def test_event_papers_post_request_with_add_action_and_without_selected_papers_raises_warning_message(self):
        session = self.client.session
        session['event_papers'] = []
        session.save()

        response = self.client.post(reverse('event_papers'), {'action': 'add'})
        self.assertTemplateUsed(response, 'report/research/add_event_papers.html')
        for message in response.context['messages']:
            self.assertEqual(message.message, _('You have selected no item. Nothing to be done!'))

    def test_event_papers_without_nira_author_list_returns_0_authors(self):
        session = self.client.session
        session['event_papers'] = [{'paper_scholar_id': self.paper.id}]
        session.save()

        self.data['action'] = 'add'
        response = self.client.post(reverse('event_papers'), self.data)

        self.assertTemplateUsed(response, 'report/research/add_event_papers.html')
        self.assertEqual(Author.objects.count(), 0)

    def test_event_papers_with_nira_author_list_returns_1_author(self):
        session = self.client.session
        session['event_papers'] = [{'paper_scholar_id': self.paper.id, 'nira_author_list': self.authors}]
        session.save()

        self.data['action'] = 'add'
        response = self.client.post(reverse('event_papers'), self.data)

        self.assertTemplateUsed(response, 'report/research/add_event_papers.html')
        self.assertEqual(Author.objects.count(), 3)

    def test_event_papers_without_paper_scholar_id_returns_0_authors(self):
        session = self.client.session
        session['event_papers'] = [{'paper_scholar_id': self.paper.id-1, 'nira_author_list': self.authors}]
        session.save()

        self.data['action'] = 'add'
        response = self.client.post(reverse('event_papers'), self.data)

        self.assertTemplateUsed(response, 'report/research/add_event_papers.html')
        self.assertEqual(Author.objects.count(), 0)

    def test_event_papers_with_start_page_and_end_page_create_published_with_them(self):
        session = self.client.session
        session['event_papers'] = [{'paper_scholar_id': self.paper.id, 'nira_author_list': self.authors}]
        session.save()

        self.assertEqual(Published.objects.count(), 0)

        self.data['action'] = 'add'
        self.client.post(reverse('event_papers'), self.data)

        published = Published.objects.last()
        self.assertEqual(Published.objects.count(), 1)
        self.assertEqual(published.start_page, int(self.data['paper_start_page_' + str(self.paper.id)][0]))
        self.assertEqual(published.end_page, int(self.data['paper_end_page_' + str(self.paper.id)][0]))
        self.assertEqual(published.article.title, self.title)

    def test_event_papers_without_start_page_and_end_page_dont_create_published_with_them(self):
        session = self.client.session
        session['event_papers'] = [{'paper_scholar_id': self.paper.id, 'nira_author_list': self.authors}]
        session.save()

        self.assertEqual(Published.objects.count(), 0)
        self.data['paper_start_page_' + str(self.paper.id)] = ''
        self.data['paper_end_page_' + str(self.paper.id)] = ''

        self.data['action'] = 'add'
        self.client.post(reverse('event_papers'), self.data)

        published = Published.objects.last()
        self.assertEqual(Published.objects.count(), 1)
        self.assertIsNone(published.start_page)
        self.assertIsNone(published.end_page)
        self.assertEqual(published.article.title, self.title)


class UpdatePapersTest(TestCase):

    def setUp(self):
        logged, self.user, self.factory = system_authentication(self)
        self.assertEqual(logged, True)

    def test_get_request_returns_import_papers_and_renders_report_research_import_html(self):
        response = self.client.get(reverse('update_papers'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report/research/import.html')

    def test_post_request_with_empty_action_returns_import_papers_and_renders_report_research_import_html(self):
        response = self.client.post(reverse('update_papers'), {'action': ''}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report/research/import.html')

    def test_post_request_with_finish_action_deletes_session_keys_and_returns_import_papers(self):
        session = self.client.session
        session['Test_key'] = 'Test_key_value'
        session.save()

        self.assertEqual(self.client.session.keys(),
                         {'_auth_user_id', '_auth_user_hash', '_auth_user_backend', 'Test_key'})

        response = self.client.post(reverse('update_papers'), {'action': 'finish'}, follow=True)

        self.assertEqual(self.client.session.keys(),
                         {'_auth_user_id', '_auth_user_hash', '_auth_user_backend'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report/research/import.html')

    def test_post_request_with_back_action_renders_report_research_add_event_papers_html(self):
        session = self.client.session
        session['event_papers'] = ['Test_event_papers']
        session.save()

        response = self.client.post(reverse('update_papers'), {'action': 'back'}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report/research/add_event_papers.html')

    def test_post_request_with_back_action_and_event_papers_renders_report_research_add_event_papers_html(self):
        person = Person.objects.create(full_name='Test person')
        paper_title = 'Test paper title'
        paper_author = 'Test paper author'
        paper = {'nira_author_list': [person], 'paper_title': paper_title, 'paper_author': paper_author}

        session = self.client.session
        session['event_papers'] = paper
        session.save()

        response = self.client.post(reverse('update_papers'), {'action': 'back'}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report/research/add_event_papers.html')

    def test_update_papers(self):

        session = self.client.session
        session['periodical_update_papers'] = 'test'
        session['event_papers'] = 'test'
        session.save()

        response = self.client.post(reverse('update_papers'), {'action': 'back'})
        self.assertEqual(response.status_code, 200)

        # Redirect status
        response = self.client.post(reverse('update_papers'), {'action': 'finish'})
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('update_papers'), {'action': 'none'})
        self.assertEqual(response.status_code, 302)


class UpdatePapersWithUpdateActionTest(TestCase):
    def setUp(self):
        self.title = 'Identifying interacting pairs of sites'
        Article.objects.create(team='s', title=self.title, research_result_type='a')

        self.paper, created = Periodical.objects.get_or_create(name='Brazilian Journal of Probab and Statistics')
        paper_id = self.paper.id

        researcher1 = Person.objects.create(full_name='Galves, A')
        researcher2 = Person.objects.create(full_name='Orlandi, E')
        researcher3 = Person.objects.create(full_name='Takahashi, DY')

        self.authors = [researcher1, researcher2, researcher3]

        self.data = {'action': 'update',
                     'paper_id': str(paper_id),
                     'paper_team_' + str(paper_id): ['s'],
                     'paper_title_' + str(paper_id): [self.title],
                     'paper_author_' + str(paper_id): self.authors,
                     'paper_periodical_' + str(paper_id): paper_id,
                     'paper_volume_' + str(paper_id): ['29'],
                     'paper_issue_' + str(paper_id): ['2'],
                     'paper_start_page_' + str(paper_id): ['443'],
                     'paper_end_page_' + str(paper_id): ['459'],
                     'paper_date_' + str(paper_id): ['2015-01-06']}

    def add_variable_to_session(self, authors):
        session = self.client.session
        session['periodical_update_papers'] = [{'paper_scholar_id': self.paper.id, 'nira_author_list': authors}]
        session.save()

    def test_update_request_with_no_periodical_raises_error_message(self):
        self.add_variable_to_session(self.authors)
        self.data['paper_periodical_%s' % str(self.paper.id)] = 'none'
        response = self.client.post(reverse('update_papers'), self.data)

        for message in response.context['messages']:
            self.assertEqual(message.message, _('You should select a journal for the paper "%s".') % self.title)

    def test_update_request_with_wrong_date_format_raises_error_message(self):
        self.add_variable_to_session(self.authors)
        self.data['paper_date_%s' % str(self.paper.id)] = ['06-01-2015']
        response = self.client.post(reverse('update_papers'), self.data)

        for message in response.context['messages']:
            self.assertEqual(message.message, _('The date field is empty or has an incorrect format for the '
                                                'paper "%s". It should be YYYY-MM-DD.') % self.title)

    def test_update_request_with_wrong_date_format_and_no_periodical_raises_error_message(self):
        self.add_variable_to_session(self.authors)
        self.data['paper_periodical_%s' % str(self.paper.id)] = 'none'
        self.data['paper_date_%s' % str(self.paper.id)] = ['06-01-2015']
        response = self.client.post(reverse('update_papers'), self.data)

        for message in response.context['messages']:
            self.assertEqual(message.message, _('The paper "%s" has no journal and the date field is empty or '
                                                'has an incorrect format') % self.title)

    def test_update_request_without_paper_id_raises_error_message(self):
        self.add_variable_to_session(self.authors)
        del self.data['paper_id']
        response = self.client.post(reverse('update_papers'), self.data)

        for message in response.context['messages']:
            self.assertEqual(message.message, _('You have selected no item. Nothing to be done!'))

    def test_update_request_without_nira_author_renders_periodical_update_papers_html(self):
        self.add_variable_to_session(self.authors)
        session = self.client.session
        session['periodical_update_papers'] = [{'paper_scholar_id': self.paper.id}]
        session.save()

        response = self.client.post(reverse('update_papers'), self.data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report/research/periodical_update_papers.html')

    def test_update_request_without_nira_author_renders_periodical_update_papers_html2(self):
        self.add_variable_to_session(self.authors)
        session = self.client.session
        session['periodical_update_papers'] = [{'paper_scholar_id': self.paper.id+1}]
        session.save()

        response = self.client.post(reverse('update_papers'), self.data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report/research/periodical_update_papers.html')

    def test_update_request_to_update_paper_authors(self):
        self.add_variable_to_session(self.authors)
        person = Person.objects.create(full_name='Antonio Galves')
        research_result = ResearchResult.objects.first()
        Author.objects.create(author=person, order=1, research_result=research_result)
        research_result.person.add(person)
        research_result.save()

        response = self.client.post(reverse('update_papers'), self.data)

        self.assertTemplateUsed(response, 'report/research/periodical_update_papers.html')

    def test_update_request_to_update_paper_authors_with_no_authors(self):
        self.add_variable_to_session(self.authors)
        response = self.client.post(reverse('update_papers'), self.data)

        self.assertTemplateUsed(response, 'report/research/periodical_update_papers.html')

    def test_update_request_with_start_and_end_page_creates_published_in_periodical_with_start_and_end_page(self):
        self.add_variable_to_session(self.authors)

        self.assertEqual(PublishedInPeriodical.objects.count(), 0)
        self.client.post(reverse('update_papers'), self.data)

        published_in_periodical = PublishedInPeriodical.objects.last()
        self.assertEqual(PublishedInPeriodical.objects.count(), 1)
        self.assertEqual(published_in_periodical.start_page, 443)
        self.assertEqual(published_in_periodical.end_page, 459)

    def test_update_request_without_start_and_end_page_creates_published_in_periodical_without_start_and_end_page(self):
        self.add_variable_to_session(self.authors)

        self.assertEqual(PublishedInPeriodical.objects.count(), 0)
        self.data['paper_start_page_' + str(self.paper.id)] = ''
        self.data['paper_end_page_' + str(self.paper.id)] = ''
        self.client.post(reverse('update_papers'), self.data)

        published_in_periodical = PublishedInPeriodical.objects.last()
        self.assertEqual(PublishedInPeriodical.objects.count(), 1)
        self.assertIsNone(published_in_periodical.start_page)
        self.assertIsNone(published_in_periodical.end_page)


class CacheTest(TestCase):

    def setUp(self):
        logged, self.user, self.factory = system_authentication(self)
        self.assertEqual(logged, True)

        session = testing_session(self)
        session.save()

    def test_major_cache(self):
        request = self.factory.post(reverse('import_papers'), {'file': TEST_FILE})
        request.user = self.user
        request.session = {}
        request.resolver_match = mock.Mock()
        request.resolver_match.url_name = "import_papers"

        response = import_papers(request)
        self.assertEqual(response.status_code, 200)

        # We need a paper as a draft in our base for update
        base_article = Article(team='s',
                               title='Identifying interacting pairs of sites in Ising models on a countable set',
                               research_result_type='a')
        base_article.save()
        base_draft = Draft(article=base_article, date='2014-07-01')
        base_draft.save()

        # Action add, in add_periodicals
        response = self.client.post(reverse('add_periodicals'),
                                    {'action': 'add',
                                    'periodicals_to_add': 'Journal of Statistical Physics'})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('add_periodicals'),
                                    {'action': 'add',
                                    'periodicals_to_add': 'Brazilian Journal of Probability and Statistics'})
        self.assertEqual(response.status_code, 200)

        # Action next, in add_periodicals
        response = self.client.post(reverse('add_periodicals'), {'action': 'next'})
        self.assertEqual(response.status_code, 200)

        # Action next, in add_papers
        response = self.client.post(reverse('add_papers'), {'action': 'next'})
        self.assertEqual(response.status_code, 200)

        # Action add, in periodical_published_papers: needs paper_ids of the selected papers to add
        paper_periodical = Periodical.objects.get(name='Journal of Statistical Physics')
        paper_periodical_id = paper_periodical.id
        response = self.client.post(reverse('periodical_published_papers'),
                                    {'action': 'add',
                                     'paper_id': u'0',
                                     'paper_team_0': [u's'],
                                     'paper_title_0': [u'Infinite systems of interacting chains with memory of '
                                                       u'variable for biological neural nets'],
                                     'paper_author_0': [u'Galves, A; L\xf6cherbach, E.'],
                                     'paper_periodical_0': paper_periodical_id,
                                     'paper_volume_0': [u'151'],
                                     'paper_issue_0': [u'5'],
                                     'paper_start_page_0': [u'896'],
                                     'paper_end_page_0': [u'921'],
                                     'paper_date_0': [u'2013-06-01']})
        self.assertEqual(response.status_code, 200)

        # Action add, in arxiv_papers, needs paper_id of the selected papers
        response = self.client.post(reverse('arxiv_papers'),
                                    {'action': 'add', 'paper_id': u'0', 'paper_team_0': [u's'],
                                     'paper_title_0': [u'Computationally efficient change point detection for '
                                                       u'high-dimensional regression'],
                                     'paper_author_0': [u'Leonardi, F; B\xfchlmann, P.'],
                                     'paper_arxiv_0': [u'http://arxiv.org/abs/1601.03704'],
                                     'paper_date_0': [u'2016-01-14']})
        self.assertEqual(response.status_code, 200)

        # Action add, in event_papers: needs paper_id of the selected papers to add
        event = Event(name='PROCEEDINGS OF THE INTERNATIONAL CONFERENCE ON NUMERICAL ANALYSIS AND APPLIED '
                           'MATHEMATICS 2014 (ICNAAM-2014)',
                      start_date='2014-09-22', end_date='2014-09-28')
        event.save()

        response = self.client.post(reverse('event_papers'),
                                    {'action': 'add', 'paper_id': u'0',
                                     'paper_team_0': [u's'],
                                     'paper_title_0': [u'Combining multivariate Markov chains'],
                                     'paper_author_0': [u'García, JE'],
                                     'paper_event_0': [str(event.id)],
                                     'paper_start_page_0': [u'60003'],
                                     'paper_end_page_0': [u'60004']})
        self.assertEqual(response.status_code, 200)

        # Action update, in update_papers: needs paper_id of the selected papers to update
        paper_periodical = Periodical.objects.get(name='Brazilian Journal of Probability and Statistics')
        paper_periodical_id = paper_periodical.id
        response = self.client.post(reverse('update_papers'),
                                    {'action': 'update', 'paper_id': u'0',
                                     'paper_team_0': [u's'],
                                     'paper_title_0':
                                         [u'Identifying interacting pairs of sites in Ising models on a countable set'],
                                     'paper_author_0': [u'Galves, A; Orlandi, E; Takahashi, DY.'],
                                     'paper_periodical_0': paper_periodical_id,
                                     'paper_volume_0': [u'29'],
                                     'paper_issue_0': [u'2'],
                                     'paper_start_page_0': [u'443'],
                                     'paper_end_page_0': [u'459'],
                                     'paper_date_0': [u'2015-01-06']})
        self.assertEqual(response.status_code, 200)


class SuperResearchResultTest(TestCase):
    def test_super_research_result_returns_empty_list_when_user_is_superuser_and_not_nira_admin(self):
        logged, self.user, self.factory = system_authentication(self)
        article_admin = ArticleAdmin(Article, AdminSite())

        qs = article_admin.get_queryset(self)
        self.assertEqual(list(qs), [])

    def test_super_research_result_returns_empty_list_when_user_is_nira_admin_and_not_superuser(self):
        logged, self.user, self.factory = system_authentication(self)
        self.user.is_nira_admin = True
        self.user.is_superuser = False
        self.user.save()
        article_admin = ArticleAdmin(Article, AdminSite())

        qs = article_admin.get_queryset(self)
        self.assertEqual(list(qs), [])

    def test_super_research_result_returns_empty_list_when_user_is_not_nira_admin_and_is_not_superuser(self):
        logged, self.user, self.factory = system_authentication(self)
        self.user.is_superuser = False
        self.user.save()
        article_admin = ArticleAdmin(Article, AdminSite())

        qs = article_admin.get_queryset(self)
        self.assertEqual(list(qs), [])

    def test_get_fieldsets_doesnt_return_ris_file_authors_or_hide_if_user_dont_have_special_permissions(self):
        logged, self.user, self.factory = system_authentication(self)
        self.user.is_superuser = False
        self.user.save()
        article_admin = ArticleAdmin(Article, AdminSite())

        qs = article_admin.get_fieldsets(self)
        self.assertEqual(
            list(qs[0][1]['fields']),
            ['team', 'title', 'status', 'type', 'periodical', 'event', 'url', 'note'])

    def test_get_fieldsets_returns_ris_file_authors_and_hide_if_user_is_superuser(self):
        logged, self.user, self.factory = system_authentication(self)
        article_admin = ArticleAdmin(Article, AdminSite())

        qs = article_admin.get_fieldsets(self)
        self.assertEqual(
            list(qs[0][1]['fields']),
            ['team', 'title', 'status', 'type', 'periodical', 'event', 'url', 'note', 'ris_file_authors', 'hide'])

    def test_get_fieldsets_returns_ris_file_authors_and_hide_if_user_is_nira_admin(self):
        logged, self.user, self.factory = system_authentication(self)
        self.user.is_superuser = False
        self.user.is_nira_admin = True
        self.user.save()
        article_admin = ArticleAdmin(Article, AdminSite())

        qs = article_admin.get_fieldsets(self)
        self.assertEqual(
            list(qs[0][1]['fields']),
            ['team', 'title', 'status', 'type', 'periodical', 'event', 'url', 'note', 'ris_file_authors', 'hide'])

    def test_get_fieldsets_returns_ris_file_authors_and_hide_if_user_is_nira_admin_and_superuser(self):
        logged, self.user, self.factory = system_authentication(self)
        self.user.is_nira_admin = True
        self.user.save()
        article_admin = ArticleAdmin(Article, AdminSite())

        qs = article_admin.get_fieldsets(self)
        self.assertEqual(
            list(qs[0][1]['fields']),
            ['team', 'title', 'status', 'type', 'periodical', 'event', 'url', 'note', 'ris_file_authors', 'hide'])


class AcademicWorkAdminTest(TestCase):
    def setUp(self):
        self.academic_work_type = TypeAcademicWork.objects.create(name='Post-doctoral')

        self.advisee = Person.objects.create(full_name='John Smith')

        self.advisor = Person.objects.create(full_name='Emma Miller')

        self.co_advisor = Person.objects.create(full_name='Emma Smith')

        self.abstract = 'Mussum ipsum cacilds, vidis litro abertis. Consetis adipiscings elitis.'

        self.team = "s"

        place_of_publication = Periodical.objects.create(name="Scientific America")
        place_of_publication.save()

        # First academic work
        self.postdoc_01 = create_postdoc(self.academic_work_type, 'postdoc_01', self.advisee, self.advisor,
                                         '2018-07-01', '2019-10-19', self.abstract)

        self.postdoc_01.co_advisor.add(self.co_advisor)

    def test_return_all_academic_works_if_user_requesting_is_superuser(self):
        logged, self.user, self.factory = system_authentication(self)
        academic_work_admin = AcademicWorkAdmin(AcademicWork, AdminSite())

        qs = academic_work_admin.get_queryset(self)
        self.assertEqual(qs[0].title, 'postdoc_01')

    def test_return_all_academic_works_if_user_requesting_is_nira_admin(self):
        logged, self.user, self.factory = system_authentication(self)
        self.user.is_superuser = False
        self.user.is_nira_admin = True
        self.user.save()
        academic_work_admin = AcademicWorkAdmin(AcademicWork, AdminSite())

        qs = academic_work_admin.get_queryset(self)
        self.assertEqual(qs[0].title, 'postdoc_01')

    def test_return_none_academic_works_if_user_requesting_is_neither_nira_admin_or_superuser(self):
        logged, self.user, self.factory = system_authentication(self)
        self.user.is_superuser = False
        self.user.save()
        academic_work_admin = AcademicWorkAdmin(AcademicWork, AdminSite())

        qs = academic_work_admin.get_queryset(self)
        self.assertEqual(list(qs), [])

    def test_returns_academic_work_of_the_user_requesting_is_advisee_and_not_superuser_or_nira_admin(
            self):
        logged, self.user, self.factory = system_authentication(self)
        self.user.is_superuser = False
        self.user.user_profile_id = self.advisee.id
        self.user.save()

        academic_work_admin = AcademicWorkAdmin(AcademicWork, AdminSite())

        qs = academic_work_admin.get_queryset(self)
        self.assertEqual(qs[0].title, 'postdoc_01')

    def test_returns_academic_work_of_the_user_requesting_is_advisor_and_not_superuser_or_nira_admin(
            self):
        logged, self.user, self.factory = system_authentication(self)
        self.user.is_superuser = False
        self.user.user_profile_id = self.advisor.id
        self.user.save()

        academic_work_admin = AcademicWorkAdmin(AcademicWork, AdminSite())

        qs = academic_work_admin.get_queryset(self)
        self.assertEqual(qs[0].title, 'postdoc_01')

    def test_returns_academic_work_of_the_user_requesting_is_co_advisor_and_not_superuser_or_nira_admin(
            self):
        logged, self.user, self.factory = system_authentication(self)
        self.user.is_superuser = False
        self.user.user_profile_id = self.co_advisor.id
        self.user.save()

        academic_work_admin = AcademicWorkAdmin(AcademicWork, AdminSite())

        qs = academic_work_admin.get_queryset(self)
        self.assertEqual(qs[0].title, 'postdoc_01')
