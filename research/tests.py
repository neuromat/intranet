from custom_auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory
from models import AcademicWork, TypeAcademicWork, Person, Article, Draft, Submitted, Accepted, PublishedInPeriodical, Periodical


USERNAME = 'myuser'
PASSWORD = 'mypassword'

# DRY way for testing

def createPostdoc(type, title, advisee, advisor, start_date, end_date):
        postdoc = AcademicWork()
        postdoc.type = type
        postdoc.title = title
        postdoc.advisee = advisee
        postdoc.advisor = advisor
        postdoc.start_date = start_date
        postdoc.end_date = end_date
        postdoc.save()
        return postdoc

def createArticle(title, team):
   article = Article(title=title, team=team)
   article.save()
   return article

def createHiddenArticle(title, team):
   article = Article(title=title, team=team, hide=True)
   article.save()
   return article

def createDraft(article, date):
    draft = Draft(article=article, date=date)
    draft.save()
    return draft

def createSubmitted(article, date):
    submitted = Submitted(article=article, date=date)
    submitted.save()
    return submitted

def createAccepted(article, date):
    accepted = Accepted(article=article, date=date)
    # Why is this necessary?
    article.type = 'p'
    article.save()
    accepted.save()
    return accepted

def createPublishedInPeriodical(article, date, placeOfPublication):
    published = PublishedInPeriodical(article=article, date=date)
    published.save()
    article.periodical = placeOfPublication
    article.type = 'p'
    article.save()
    return published

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
        self.postdoc_01 = createPostdoc(academic_work, 'postdoc_01', advisee, advisor, '2013-08-20', '2014-08-26')

        # Second academic work
        self.postdoc_02 = createPostdoc(academic_work,'postdoc_02', advisee, advisor, '2013-07-01', '2014-05-26')

        # Third academic work
        self.postdoc_03 = createPostdoc(academic_work, 'postdoc_03', advisee, advisor, '2014-08-05', '2015-06-20')

        # Fourth academic work
        self.postdoc_04 = createPostdoc(academic_work, 'postdoc_04', advisee, advisor, '2015-06-25', '2016-01-01')

        # Fifth academic work
        self.postdoc_05 = createPostdoc(academic_work, 'postdoc_05', advisee, advisor, '2015-08-26', '2016-01-01')

        # Sixth academic work
        self.postdoc_06 = createPostdoc(academic_work, 'postdoc_06', advisee, advisor, '2013-05-20', '2016-01-01')

        # Seventh academic work
        self.postdoc_07 = createPostdoc(academic_work, 'postdoc_07', advisee, advisor, '2013-07-01', '2014-07-01')

        # Eighth academic work
        self.postdoc_08 = createPostdoc(academic_work, 'postdoc_08', advisee, advisor, '2014-07-01', '2016-01-01')

        # List of articles

        # First Article: Draft(20/12/12), Submitted(05/01/14), Accepted(05/01/15), Published(05/11/15)
        self.article_01 = createArticle('Artigo 01', team)
        self.draft_01 = createDraft(self.article_01, '2012-12-20')
        self.submitted_01 = createSubmitted(self.article_01, '2014-01-05')
        self.accepted_01 = createAccepted(self.article_01, '2015-01-05')
        self.published_01 = createPublishedInPeriodical(self.article_01, '2015-11-05', place_of_publication)

        # Second Article: Submitted(31/07/14)
        self.article_02 = createArticle('Article 02', team)
        self.submitted_02 = createSubmitted(self.article_02, '2014-07-31')

        # Third Article: Accepted(31/07/14), Published(05/11/15)
        self.article_03 = createArticle('Article 03', team)
        self.accepted_03 = createAccepted(self.article_03,'2014-07-31')
        self.published_03 = createPublishedInPeriodical(self.article_03, '2015-11-15', place_of_publication)

        # Fourth Article: Draft(01/06/14), Published(01/08/15)
        self.article_04 = createArticle('Article 04', team)
        self.draft_04 = createDraft(self.article_04, '2014-06-01')
        self.published_04 = createPublishedInPeriodical(self.article_04, '2015-08-01', place_of_publication)

        # Fifth Article: Draft(01/06/14), Published(01/08/15)
        self.article_05 = createArticle('Article 05', team)
        self.draft_05 = createDraft(self.article_05, '2014-06-01')
        self.published_05 = createPublishedInPeriodical(self.article_05,'2015-08-01', place_of_publication)

        # Sixth Article: Published(30/06/14)
        self.article_06 = createArticle('Article 06', team)
        self.published_06 = createPublishedInPeriodical(self.article_06, '2014-06-30', place_of_publication)

        # Seventh Article: Published(01/07/14)
        self.article_07 = createArticle('Article 07', team)
        self.published_07 = createPublishedInPeriodical(self.article_07, '2014-07-01', place_of_publication)

        # Eighth Article: Draft(30/06/14)
        self.article_08 = createArticle('Article 08', team)
        self.draft_08 = createDraft(self.article_08, '2014-06-30')

        # Nineth Article: Draft(30/06/14)
        self.article_09 = createHiddenArticle('Article 09', team)
        self.draft_09 = createDraft(self.article_09, '2014-06-30')

    def test_current_academic_works_report(self):
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