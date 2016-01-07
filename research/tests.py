from custom_auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory
from models import AcademicWork, TypeAcademicWork, Person, Article, Draft, Submitted, Accepted, PublishedInPeriodical, Periodical


USERNAME = 'myuser'
PASSWORD = 'mypassword'


class ResearchValidation(TestCase):
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

    draft_01 = None
    draft_04 = None
    draft_05 = None
    draft_08 = None

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
        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD)
        self.user.is_active = True
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()

        self.factory = RequestFactory()

        logged = self.client.login(username=USERNAME, password=PASSWORD)
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
        self.postdoc_01 = AcademicWork()
        self.postdoc_01.type = academic_work
        self.postdoc_01.title = 'postdoc_01'
        self.postdoc_01.advisee = advisee
        self.postdoc_01.advisor = advisor
        self.postdoc_01.start_date = '2013-08-20'
        self.postdoc_01.end_date = '2014-08-26'
        self.postdoc_01.save()

        # Second academic work
        self.postdoc_02 = AcademicWork()
        self.postdoc_02.type = academic_work
        self.postdoc_02.title = 'postdoc_02'
        self.postdoc_02.advisee = advisee
        self.postdoc_02.advisor = advisor
        self.postdoc_02.start_date = '2013-07-01'
        self.postdoc_02.end_date = '2014-05-26'
        self.postdoc_02.save()

        # Third academic work
        self.postdoc_03 = AcademicWork()
        self.postdoc_03.type = academic_work
        self.postdoc_03.title = 'postdoc_03'
        self.postdoc_03.advisee = advisee
        self.postdoc_03.advisor = advisor
        self.postdoc_03.start_date = '2014-08-05'
        self.postdoc_03.end_date = '2015-06-20'
        self.postdoc_03.save()

        # Fourth academic work
        self.postdoc_04 = AcademicWork()
        self.postdoc_04.type = academic_work
        self.postdoc_04.title = 'postdoc_04'
        self.postdoc_04.advisee = advisee
        self.postdoc_04.advisor = advisor
        self.postdoc_04.start_date = '2015-06-25'
        self.postdoc_04.end_date = '2016-01-01'
        self.postdoc_04.save()

        # Fifth academic work
        self.postdoc_05 = AcademicWork()
        self.postdoc_05.type = academic_work
        self.postdoc_05.title = 'postdoc_05'
        self.postdoc_05.advisee = advisee
        self.postdoc_05.advisor = advisor
        self.postdoc_05.start_date = '2015-08-26'
        self.postdoc_05.end_date = '2016-01-01'
        self.postdoc_05.save()

        # Sixth academic work
        self.postdoc_06 = AcademicWork()
        self.postdoc_06.type = academic_work
        self.postdoc_06.title = 'postdoc_06'
        self.postdoc_06.advisee = advisee
        self.postdoc_06.advisor = advisor
        self.postdoc_06.start_date = '2013-05-20'
        self.postdoc_06.end_date = '2016-01-01'
        self.postdoc_06.save()

        # Seventh academic work
        self.postdoc_07 = AcademicWork()
        self.postdoc_07.type = academic_work
        self.postdoc_07.title = 'postdoc_07'
        self.postdoc_07.advisee = advisee
        self.postdoc_07.advisor = advisor
        self.postdoc_07.start_date = '2013-07-01'
        self.postdoc_07.end_date = '2014-07-01'
        self.postdoc_07.save()

        # Eighth academic work
        self.postdoc_08 = AcademicWork()
        self.postdoc_08.type = academic_work
        self.postdoc_08.title = 'postdoc_08'
        self.postdoc_08.advisee = advisee
        self.postdoc_08.advisor = advisor
        self.postdoc_08.start_date = '2014-07-01'
        self.postdoc_08.end_date = '2016-01-01'
        self.postdoc_08.save()

        # First Article: Draft(20/12/12), Submitted(05/01/14), Accepted(05/01/15), Published(05/11/15)
        self.article_01 = Article(title='Artigo 01', team=team)
        self.article_01.save()
        self.draft_01 = Draft(article=self.article_01, date='2012-12-20')
        self.draft_01.save()
        self.submitted_01 = Submitted(article=self.article_01, date='2014-01-05')
        self.submitted_01.save()
        self.accepted_01 = Accepted(article=self.article_01, date='2015-01-05')
        self.accepted_01.save()
        self.published_01 = PublishedInPeriodical(article=self.article_01, date='2015-11-05')
        self.article_01.periodical = place_of_publication

        # Second Article: Submitted(31/07/14)
        self.article_02 = Article(title='Article 02', team=team)
        self.article_02.save()
        self.submitted_02 = Submitted(article=self.article_02, date='2014-07-31')
        self.submitted_02.save()

        # Third Article: Accepted(31/07/14), Published(05/11/15)
        self.article_03 = Article(title='Article 03', team=team)
        self.accepted_03 = Accepted(article=self.article_03, date='2014-07-31')
        self.published_03 = PublishedInPeriodical(article=self.article_03, date='2015-11-15')
        self.article_03.periodical = place_of_publication

        # Fourth Article: Draft(01/06/14), Published(01/08/15)
        self.article_04 = Article(title='Article 04', team=team)
        self.draft_04 = Draft(article=self.article_04, date='2014-06-01')
        self.published_04 = PublishedInPeriodical(article=self.article_04, date='2015-08-01')
        self.article_04.periodical = place_of_publication

        # Fifth Article: Draft(01/06/14), Published(01/08/15)
        self.article_05 = Article(title='Article 05', team=team)
        self.draft_05 = Draft(article=self.article_05, date='2014-06-01')
        self.published_05 = PublishedInPeriodical(article=self.article_05,date='2015-08-01')
        self.article_05.periodical = place_of_publication

        # Sixth Article: Published(30/06/14)
        self.article_06 = Article(title='Article 06', team=team)
        self.published_06 = PublishedInPeriodical(article=self.article_06, date='2014-06-30')

        # Seventh Article: Published(01/07/14)
        self.article_07 = Article(title='Article 07', team=team)
        self.published_07 = PublishedInPeriodical(article=self.article_07, date='2014-07-01')

        # Eighth Article: Draft(30/06/14)
        self.article_08 = Article(title='Article 08', team=team)
        self.draft_08 = Draft(article=self.article_08, date='2014-06-30')

    def test_current_report(self):
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

    def test_previous_report(self):
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

    def test_articles_in_certain_period(self):
        start_date = '01-07-2014'
        end_date = '31-07-2015'

        response = self.client.post(reverse('articles'), {'start_date': start_date, 'end_date': end_date})

        # self.assertEqual(len(response.context['published_scientific']), 1)
        self.assertEqual(len(response.context['submitted_scientific']), 1)

