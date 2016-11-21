# -*- coding: utf-8 -*-
import datetime
from custom_auth.models import User
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory
from research.models import AcademicWork, TypeAcademicWork, Person, Article, Draft, Event, Submitted, Accepted, \
                            PublishedInPeriodical, Periodical
from research.views import scholar, scholar_info, now_plus_five_years, arxiv, import_papers


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
        self.postdoc_01 = create_postdoc(academic_work, 'postdoc_01', advisee, advisor, '2013-08-20', '2014-08-26',
                                         abstract)

        # Second academic work
        self.postdoc_02 = create_postdoc(academic_work, 'postdoc_02', advisee, advisor, '2013-07-01', '2014-05-26',
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
        start_date = '01/07/2014'
        end_date = '31/07/2015'

        response = self.client.post(reverse('academic_works'), {'start_date': start_date, 'end_date': end_date})

        self.assertEqual(len(response.context['postdoc_concluded']), 3)
        self.assertEqual(len(response.context['postdoc_in_progress']), 3)

        titles_concluded = [item.title for item in response.context['postdoc_concluded']]
        self.assertTrue(self.postdoc_01.title in titles_concluded)
        self.assertTrue(self.postdoc_03.title in titles_concluded)
        self.assertTrue(self.postdoc_07.title in titles_concluded)

        titles_in_progress = [item.title for item in response.context['postdoc_in_progress']]
        self.assertTrue(self.postdoc_04.title in titles_in_progress)
        self.assertTrue(self.postdoc_06.title in titles_in_progress)
        self.assertTrue(self.postdoc_08.title in titles_in_progress)

    def test_previous_academic_works_report(self):
        """ Report of previous academic works is fine """
        start_date = '01/07/2013'
        end_date = '01/07/2014'

        response = self.client.post(reverse('academic_works'), {'start_date': start_date, 'end_date': end_date})

        self.assertEqual(len(response.context['postdoc_concluded']), 2)
        self.assertEqual(len(response.context['postdoc_in_progress']), 3)

        titles_concluded = [item.title for item in response.context['postdoc_concluded']]
        self.assertTrue(self.postdoc_02.title in titles_concluded)
        self.assertTrue(self.postdoc_07.title in titles_concluded)

        titles_in_progress = [item.title for item in response.context['postdoc_in_progress']]
        self.assertTrue(self.postdoc_01.title in titles_in_progress)
        self.assertTrue(self.postdoc_06.title in titles_in_progress)
        self.assertTrue(self.postdoc_08.title in titles_in_progress)

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
            {'Hydrodynamic limit for interacting neurons': '/citations?view_op=view_citation&amp;hl=pt-BR&amp;oe=ASCII&'
                                                           'amp;user=OaY57UIAAAAJ&amp;pagesize=100&amp;citation_for_'
                                                           'view=OaY57UIAAAAJ:u-x6o8ySG0sC'},
            {'The solution of the complete nontrivial cycle intersection problem for permutations':
             '/citations?view_op=view_citation&amp;hl=pt-BR&amp;oe=ASCII&amp;user=OaY57UIAAAAJ&amp;pagesize=100&amp;'
             'citation_for_view=OaY57UIAAAAJ:J_g5lzvAfSwC'},
            {'Infinite systems of interacting chains with memory of variable length\xe2\x80\x94a stochastic model '
             'for biological neural nets': '/citations?view_op=view_citation&amp;hl=pt-BR&amp;oe=ASCII&amp;user=OaY57UI'
                                           'AAAAJ&amp;pagesize=100&amp;citation_for_view=OaY57UIAAAAJ:u5HHmVD_uO8C'}]
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
            scholar_titles.append(paper.keys()[0])

        for paper in self.papers_list:
            if paper.keys()[0] in scholar_titles:
                ret = True
            else:
                ret = False

        self.valid_scholar_list.extend(scholar_list)
        self.assertTrue(ret)

    def test_get_paper_info(self):
        """
        Are we getting the paper date and url successfully?
        Obs: this test depends on test_get_papers
        """
        scholar_list = scholar()
        result = scholar_info(scholar_list, self.specific_paper_title)
        self.assertEqual(result[0], self.specific_paper_date)
        self.assertEqual(result[1], self.specific_paper_link)
        self.assertNotEqual(result[0], self.wrong_paper_date)
        self.assertNotEqual(result[1], self.wrong_paper_date)


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
        logged, self.user, self.factory = system_authentication(self)
        self.assertEqual(logged, True)

    def test_event_papers(self):

        session = self.client.session
        session['event_papers'] = []
        session['arxiv_papers'] = []
        session['periodical_update_papers'] = []
        session.save()

        response = self.client.post(reverse('event_papers'), {'action': 'next'})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('event_papers'), {'action': 'back'})
        self.assertEqual(response.status_code, 200)


class UpdatePapersTest(TestCase):

    def setUp(self):
        logged, self.user, self.factory = system_authentication(self)
        self.assertEqual(logged, True)

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
                                     'paper_event_0': [u'1'],
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
