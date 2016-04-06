import datetime, os
from custom_auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from research.models import AcademicWork, TypeAcademicWork, Person, Article, Draft, Submitted, Accepted, \
PublishedInPeriodical, Periodical
from research.views import scholar, scholar_info, valid_date, now_plus_five_years, arxiv, import_papers
from django.core.files.uploadedfile import SimpleUploadedFile


USERNAME = 'myuser'
PASSWORD = 'mypassword'


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


def create_postdoc(type, title, advisee, advisor, start_date, end_date):
    postdoc = AcademicWork()
    postdoc.type = type
    postdoc.title = title
    postdoc.advisee = advisee
    postdoc.advisor = advisor
    postdoc.start_date = start_date
    postdoc.end_date = end_date
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

        team = "s"

        place_of_publication = Periodical.objects.create(name="Scientific America")
        place_of_publication.save()

        # List of academic works

        # First academic work
        self.postdoc_01 = create_postdoc(academic_work, 'postdoc_01', advisee, advisor, '2013-08-20', '2014-08-26')

        # Second academic work
        self.postdoc_02 = create_postdoc(academic_work, 'postdoc_02', advisee, advisor, '2013-07-01', '2014-05-26')

        # Third academic work
        self.postdoc_03 = create_postdoc(academic_work, 'postdoc_03', advisee, advisor, '2014-08-05', '2015-06-20')

        # Fourth academic work
        self.postdoc_04 = create_postdoc(academic_work, 'postdoc_04', advisee, advisor, '2015-06-25', '2016-01-01')

        # Fifth academic work
        self.postdoc_05 = create_postdoc(academic_work, 'postdoc_05', advisee, advisor, '2015-08-26', '2016-01-01')

        # Sixth academic work
        self.postdoc_06 = create_postdoc(academic_work, 'postdoc_06', advisee, advisor, '2013-05-20', '2016-01-01')

        # Seventh academic work
        self.postdoc_07 = create_postdoc(academic_work, 'postdoc_07', advisee, advisor, '2013-07-01', '2014-07-01')

        # Eighth academic work
        self.postdoc_08 = create_postdoc(academic_work, 'postdoc_08', advisee, advisor, '2014-07-01', '2016-01-01')

        # List of articles

        # First Article: Draft(20/12/12), Submitted(05/01/14), Accepted(05/01/15), Published(05/11/15)
        self.article_01 = create_article('Artigo 01', team)
        self.draft_01 = create_draft(self.article_01, '2012-12-20')
        self.submitted_01 = create_submitted(self.article_01, '2014-01-05')
        self.accepted_01 = create_accepted(self.article_01, '2015-01-05')
        self.published_01 = create_published_in_periodical(self.article_01, '2015-11-05', place_of_publication)

        # Second Article: Submitted(31/07/14)
        self.article_02 = create_article('Article 02', team)
        self.submitted_02 = create_submitted(self.article_02, '2014-07-31')

        # Third Article: Accepted(31/07/14), Published(05/11/15)
        self.article_03 = create_article('Article 03', team)
        self.accepted_03 = create_accepted(self.article_03, '2014-07-31')
        self.published_03 = create_published_in_periodical(self.article_03, '2015-11-15', place_of_publication)

        # Fourth Article: Draft(01/06/14), Published(01/08/15)
        self.article_04 = create_article('Article 04', team)
        self.draft_04 = create_draft(self.article_04, '2014-06-01')
        self.published_04 = create_published_in_periodical(self.article_04, '2015-08-01', place_of_publication)

        # Fifth Article: Draft(01/06/14), Published(01/08/15)
        self.article_05 = create_article('Article 05', team)
        self.draft_05 = create_draft(self.article_05, '2014-06-01')
        self.published_05 = create_published_in_periodical(self.article_05, '2015-08-01', place_of_publication)

        # Sixth Article: Published(30/06/14)
        self.article_06 = create_article('Article 06', team)
        self.published_06 = create_published_in_periodical(self.article_06, '2014-06-30', place_of_publication)

        # Seventh Article: Published(01/07/14)
        self.article_07 = create_article('Article 07', team)
        self.published_07 = create_published_in_periodical(self.article_07, '2014-07-01', place_of_publication)

        # Eighth Article: Draft(30/06/14)
        self.article_08 = create_article('Article 08', team)
        self.draft_08 = create_draft(self.article_08, '2014-06-30')

        # Nineth Article: Draft(30/06/14)
        self.article_09 = create_hidden_article('Article 09', team)
        self.draft_09 = create_draft(self.article_09, '2014-06-30')

    def test_current_academic_works_report(self):
        """ Report of current academic works is fine """
        start_date = '01-07-2014'
        end_date = '31-07-2015'

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
        start_date = '01-07-2013'
        end_date = '01-07-2014'

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
        start_date = '01-07-2014'
        end_date = '31-07-2015'

        response = self.client.post(reverse('articles'), {'start_date': start_date, 'end_date': end_date})

        self.assertEqual(len(response.context['draft_scientific']), 4)
        self.assertEqual(len(response.context['submitted_scientific']), 1)
        self.assertEqual(len(response.context['accepted_scientific']), 2)
        self.assertEqual(len(response.context['published_scientific']), 1)

        show_drafted_articles = []
        hide_drafted_articles = []

        for item in response.context['draft_scientific']:
            if item.article.hide:
                hide_drafted_articles.append(item.article.title)
            else:
                show_drafted_articles.append(item.article.title)

        self.assertTrue(self.article_04.title in show_drafted_articles)
        self.assertTrue(self.article_05.title in show_drafted_articles)
        self.assertTrue(self.article_08.title in show_drafted_articles)
        self.assertTrue(self.article_09.title in hide_drafted_articles)

        submitted_articles = [item.article.title for item in response.context['submitted_scientific']]
        self.assertTrue(self.article_02.title in submitted_articles)

        accepted_articles = [item.article.title for item in response.context['accepted_scientific']]
        self.assertTrue(self.article_01.title in accepted_articles)
        self.assertTrue(self.article_03.title in accepted_articles)

        published_articles = [item.article.title for item in response.context['published_scientific']]
        self.assertTrue(self.article_07.title in published_articles)

    def test_previous_articles_report(self):
        """ Report of previous articles is fine """
        start_date = '01-07-2013'
        end_date = '31-07-2014'

        response = self.client.post(reverse('articles'), {'start_date': start_date, 'end_date': end_date})

        self.assertEqual(len(response.context['draft_scientific']), 4)
        self.assertEqual(len(response.context['submitted_scientific']), 2)
        self.assertEqual(len(response.context['accepted_scientific']), 1)
        self.assertEqual(len(response.context['published_scientific']), 2)

        show_drafted_articles = []
        hide_drafted_articles = []

        for item in response.context['draft_scientific']:
            if item.article.hide:
                hide_drafted_articles.append(item.article.title)
            else:
                show_drafted_articles.append(item.article.title)

        self.assertTrue(self.article_04.title in show_drafted_articles)
        self.assertTrue(self.article_05.title in show_drafted_articles)
        self.assertTrue(self.article_08.title in show_drafted_articles)
        self.assertTrue(self.article_09.title in hide_drafted_articles)

        submitted_articles = [item.article.title for item in response.context['submitted_scientific']]
        self.assertTrue(self.article_01.title in submitted_articles)
        self.assertTrue(self.article_02.title in submitted_articles)

        accepted_articles = [item.article.title for item in response.context['accepted_scientific']]
        self.assertTrue(self.article_03.title in accepted_articles)

        published_articles = [item.article.title for item in response.context['published_scientific']]
        self.assertTrue(self.article_06.title in published_articles)
        self.assertTrue(self.article_07.title in published_articles)


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
        self.papers_list = [{'Hydrodynamic limit for interacting neurons': '/citations?view_op=view_citation&amp;hl=pt-BR&amp;oe=ASCII&amp;user=OaY57UIAAAAJ&amp;pagesize=100&amp;citation_for_view=OaY57UIAAAAJ:u-x6o8ySG0sC'},
                            {'The solution of the complete nontrivial cycle intersection problem for permutations': '/citations?view_op=view_citation&amp;hl=pt-BR&amp;oe=ASCII&amp;user=OaY57UIAAAAJ&amp;pagesize=100&amp;citation_for_view=OaY57UIAAAAJ:J_g5lzvAfSwC'},
                            {'Infinite systems of interacting chains with memory of variable length\xe2\x80\x94a stochastic model for biological neural nets': '/citations?view_op=view_citation&amp;hl=pt-BR&amp;oe=ASCII&amp;user=OaY57UIAAAAJ&amp;pagesize=100&amp;citation_for_view=OaY57UIAAAAJ:u5HHmVD_uO8C'}]
        self.specific_paper_title = 'Hydrodynamic limit for interacting neurons'
        self.specific_paper_date = datetime.date(2014, 1, 17)
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

    def setUp(self):
        self.date = "29/12/1995"
        self.invalid_day = "32/12/1995"
        self.invalid_month = "20/13/1995"
        self.invalid_year = "20/12/-1000"

    def test_valid_dates(self):
        """
        Test if date is valid
        """
        self.assertTrue(valid_date(self.date))
        self.assertFalse(valid_date(self.invalid_day))
        self.assertFalse(valid_date(self.invalid_month))
        self.assertFalse(valid_date(self.invalid_year))

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

        response = self.client.post(reverse('import_papers'), {'file': './research/citations.ris'})
        self.assertEqual(response.status_code, 200)

        with open('./research/citations.ris') as file:
            req = RequestFactory()
            request = req.post(reverse('import_papers'), {'file': file})
            request.user = self.user
            response = import_papers(request)
            self.assertEqual(response.status_code, 200)

        not_ris_file = SimpleUploadedFile('citations.jpg', b'rb', content_type='image/jpeg')
        response = self.client.post(reverse('import_papers'), {'file': not_ris_file})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('add_periodicals'), {'action': 'add'})
        self.assertEqual(response.status_code, 200)

        # Problems with cache on this step
        # response = self.client.post(reverse('add_periodicals'), {'action': 'next'})
        # self.assertEqual(response.status_code, 200)


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

    def test_add_papers(self):

        # Cache problems
        # response = self.client.post(reverse('add_papers'), {'action': 'next'})
        # self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('add_papers'), {'action': 'back'})
        self.assertEqual(response.status_code, 200)


class PeriodicalPublishedTest(TestCase):

    def setUp(self):
        logged, self.user, self.factory = system_authentication(self)
        self.assertEqual(logged, True)

    def test_periodical_published_papers(self):

        response = self.client.post(reverse('periodical_published_papers'), {'action': 'add'})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('periodical_published_papers'), {'action': 'next'})
        self.assertEqual(response.status_code, 200)


class ArxivPapersTest(TestCase):

    def setUp(self):
        logged, self.user, self.factory = system_authentication(self)
        self.assertEqual(logged, True)

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

        response = self.client.post(reverse('event_papers'), {'action': 'add'})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('event_papers'), {'action': 'next'})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('event_papers'), {'action': 'back'})
        self.assertEqual(response.status_code, 200)


class UpdatePapersTest(TestCase):

    def setUp(self):
        logged, self.user, self.factory = system_authentication(self)
        self.assertEqual(logged, True)

    def test_update_papers(self):

        response = self.client.post(reverse('update_papers'), {'action': 'update'})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('update_papers'), {'action': 'back'})
        self.assertEqual(response.status_code, 200)

        # Redirect status
        response = self.client.post(reverse('update_papers'), {'action': 'finish'})
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('update_papers'), {'action': 'none'})
        self.assertEqual(response.status_code, 302)