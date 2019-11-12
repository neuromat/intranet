from django.test import TestCase
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db.models import ProtectedError

from research.models import ResearchResult, Author, Book, Periodical, PeriodicalRISFile, Event, EventRISFile, \
    AcademicWork, TypeAcademicWork, Article, Draft, Submitted, Accepted, Published
from person.models import Person, CitationName, Institution, InstitutionType


class ResearchModelTests(TestCase):

    def test_type_academic_work_string_representation(self):
        name = 'PhD'
        type_academic_work = TypeAcademicWork.objects.create(name='PhD')

        self.assertEqual(type_academic_work.__str__(), name)


class ResearchResultModelTests(TestCase):
    def test_research_result_string_representation(self):
        person = Person.objects.create(full_name="Person_Test")
        title = 'Title'
        research_result = ResearchResult(
            team='s',
            title=title,
            research_result_type='a'
        )
        research_result.save()
        Author.objects.create(author=person, order=1, research_result=research_result)
        research_result.person.add(person)
        research_result.save()

        self.assertEqual(research_result.__str__(), title)

    def test_research_result_returns_authors_from_ris_file_if_there_is_any(self):
        person = Person.objects.create(full_name="Person_Test")
        title = 'Title'
        ris_file_authors = 'Test_ris_file_authors'
        research_result = ResearchResult(
            team='s',
            title=title,
            research_result_type='a'
        )
        research_result.save()
        Author.objects.create(author=person, order=1, research_result=research_result)
        research_result.person.add(person)
        research_result.ris_file_authors = ris_file_authors
        research_result.save()

        self.assertEqual(research_result.authors(), ris_file_authors)

    def test_research_result_returns_authors_citation_names_from_db_if_none_is_passed_through_ris_file(self):
        person = Person.objects.create(full_name="Person_Test")
        citation_name = 'Test, P.'
        CitationName.objects.create(person=person, name=citation_name, default_name=True)

        title = 'Title'

        research_result = ResearchResult(
            team='s',
            title=title,
            research_result_type='a'
        )
        research_result.save()
        Author.objects.create(author=person, order=1, research_result=research_result)
        research_result.person.add(person)
        research_result.save()

        self.assertEqual(research_result.authors(), citation_name)


class BookModelTests(TestCase):
    def test_book_string_representation(self):
        person = Person.objects.create(full_name="Person_Test")
        institution_type = InstitutionType.objects.create(name="Tipo")
        institution = Institution.objects.create(name='Institution', type=institution_type)
        title = 'Title'

        book = Book(
            team='s',
            title=title,
            research_result_type='a',
            type='b',
            publisher=institution,
            date=timezone.now()
        )
        book.save()
        Author.objects.create(author=person, order=1, research_result=book)
        book.person.add(person)
        book.save()

        self.assertEqual(book.__str__(), title)

    def test_book_save_sets_research_result_type_to_b(self):
        person = Person.objects.create(full_name="Person_Test")
        institution_type = InstitutionType.objects.create(name="Tipo")
        institution = Institution.objects.create(name='Institution', type=institution_type)
        title = 'Title'

        book = Book(
            team='s',
            title=title,
            research_result_type='a',
            type='b',
            publisher=institution,
            date=timezone.now()
        )

        self.assertEqual(book.research_result_type, 'a')
        book.save()
        Author.objects.create(author=person, order=1, research_result=book)
        book.person.add(person)
        book.save()

        self.assertEqual(book.research_result_type, 'b')


class PeriodicalModelTests(TestCase):
    def setUp(self):
        self.name = 'Periodical'
        self.periodical = Periodical.objects.create(name=self.name)

    def test_periodical_string_representation(self):
        self.assertEqual(self.periodical.__str__(), self.name)

    def test_periodical_ris_file_string_representation(self):
        periodical_ris_file = PeriodicalRISFile.objects.create(periodical=self.periodical, name=self.name)
        self.assertEqual(periodical_ris_file.__str__(), self.name)


class EventModelTests(TestCase):
    def setUp(self):
        self.name = 'Event'
        self.start_date = timezone.now()
        self.end_date = timezone.now() + timezone.timedelta(1)
        self.local = 'Local_test'
        self.event = Event.objects.create(
            name=self.name,
            start_date=self.start_date,
            end_date=self.end_date,
            local=self.local)

    def test_event_string_representation(self):
        self.assertEqual(self.event.__str__(), self.name)

    def test_event_ris_file_string_representation(self):
        name_ris_file = 'EventRISFile'
        event_ris_file = EventRISFile.objects.create(event=self.event, name=name_ris_file)

        self.assertEqual(event_ris_file.__str__(), name_ris_file)


class AcademicWorkModelTests(TestCase):
    def test_academic_work_string_representation(self):
        type_academic_work = TypeAcademicWork.objects.create(name='TypeAcadmicWork')
        advisee = Person.objects.create(full_name="Person_Test")
        advisor = advisee
        funding = True
        start_date = timezone.now()
        abstract = 'Abstract'
        title = 'Academic Work'

        academic_work = AcademicWork.objects.create(
            type=type_academic_work,
            advisee=advisee,
            advisor=advisor,
            funding=funding,
            start_date=start_date,
            abstract=abstract,
            title=title
        )

        self.assertEqual(academic_work.__str__(), title)


class ArticleModelTests(TestCase):
    def setUp(self):
        self.person = Person.objects.create(full_name="Person_Test")
        self.title = 'Title'

        self.article = Article(
            team='s',
            title=self.title,
            research_result_type='a',
            status='p',
            type='p'
        )
        self.article.save()
        Author.objects.create(author=self.person, order=1, research_result=self.article)
        self.article.person.add(self.person)
        self.article.save()

    def test_book_string_representation(self):
        self.assertEqual(self.article.__str__(), self.title)

    def test_article_current_status_returns_published_when_status_is_p(self):
        self.article.status = 'p'
        self.assertEqual(self.article.current_status(), _('Published'))

    def test_article_current_status_returns_accepted_when_status_is_a(self):
        self.article.status = 'a'
        self.assertEqual(self.article.current_status(), _('Accepted'))

    def test_article_current_status_returns_submitted_when_status_is_s(self):
        self.article.status = 's'
        self.assertEqual(self.article.current_status(), _('Submitted'))

    def test_article_current_status_returns_draft_when_status_is_d(self):
        self.article.status = 'd'
        self.assertEqual(self.article.current_status(), _('Draft'))

    def test_article_current_status_returns_none_if_no_status_is_passed(self):
        person = Person.objects.create(full_name="Person_Test_2")
        title = 'Title_2'

        article = Article(
            team='s',
            title=title,
            research_result_type='a'
        )
        article.save()
        Author.objects.create(author=person, order=1, research_result=article)
        article.person.add(person)
        article.save()

        self.assertIsNone(article.current_status())

    def test_type_of_article_function_returns_periodical_if_p_is_passed_to_it(self):
        self.assertEqual(self.article.type_of_article(), _('Periodical'))

    def test_type_of_article_function_returns_event_if_e_is_passed_to_it(self):
        self.article.type = 'e'
        self.assertEqual(self.article.type_of_article(), _('Event'))

    def test_type_of_article_function_returns_not_defined_if_neither_p_or_e_is_passed_to_it(self):
        self.article.type = 's'
        self.assertEqual(self.article.type_of_article(), _('Not defined'))


class ResearchAppIntegrationTest(TestCase):
    def test_do_not_delete_person_instance_if_there_is_author_associated(self):
        self.assertEqual(Person.objects.count(), 0)
        self.assertEqual(Author.objects.count(), 0)
        self.assertEqual(ResearchResult.objects.count(), 0)

        person = Person.objects.create(full_name='Person_Test')

        research_result = ResearchResult.objects.create(
            team='s',
            title='Research_Result',
            research_result_type='a')

        author = Author.objects.create(author=person, research_result=research_result, order=1)

        research_result.person.add(person)
        research_result.save()

        with self.assertRaises(ProtectedError) as e:
            person.delete()

        self.assertEqual(Person.objects.last(), person)
        self.assertEqual(Author.objects.last(), author)
        self.assertEqual(ResearchResult.objects.last(), research_result)

    def test_do_not_delete_institution_instance_if_there_is_book_associated(self):
        self.assertEqual(InstitutionType.objects.count(), 0)
        self.assertEqual(Institution.objects.count(), 0)
        self.assertEqual(Book.objects.count(), 0)

        institution_type = InstitutionType.objects.create(name='Institution_Type_Test')
        institution = Institution.objects.create(name='Institution_Test', type=institution_type)

        book = Book.objects.create(
            team='s',
            title='Book',
            research_result_type='b',
            date=timezone.now(),
            publisher=institution,
            type='b'
        )

        with self.assertRaises(ProtectedError) as e:
            institution.delete()

        self.assertEqual(InstitutionType.objects.last(), institution_type)
        self.assertEqual(Institution.objects.last(), institution)
        self.assertEqual(Book.objects.last(), book)
        self.assertEqual(Book.objects.last().publisher, institution)

    def test_do_not_delete_institution_instance_if_there_is_event_associated(self):
        self.assertEqual(InstitutionType.objects.count(), 0)
        self.assertEqual(Institution.objects.count(), 0)
        self.assertEqual(Event.objects.count(), 0)

        institution_type = InstitutionType.objects.create(name='Institution_Type_Test')
        institution = Institution.objects.create(name='Institution_Test', type=institution_type)

        event = Event.objects.create(
            name='Event_Test',
            publisher=institution,
            start_date=timezone.now(),
            end_date=timezone.now(),
            local='Algum Lugar, Planeta Terra'
        )

        with self.assertRaises(ProtectedError) as e:
            institution.delete()

        self.assertEqual(InstitutionType.objects.last(), institution_type)
        self.assertEqual(Institution.objects.last(), institution)
        self.assertEqual(Event.objects.last(), event)
        self.assertEqual(Event.objects.last().publisher, institution)

    def test_do_not_delete_periodical_if_there_is_article_associated(self):
        self.assertEqual(Periodical.objects.count(), 0)
        self.assertEqual(Article.objects.count(), 0)

        periodical = Periodical.objects.create(name='Periodical_Test')

        article = Article.objects.create(
            team='s',
            title='Article_Test',
            research_result_type='a',
            periodical=periodical,
            status='Status_Test'
        )

        with self.assertRaises(ProtectedError) as e:
            periodical.delete()

        self.assertEqual(Periodical.objects.last(), periodical)
        self.assertEqual(Article.objects.last(), article)
        self.assertEqual(Article.objects.last().periodical, periodical)

    def test_do_not_delete_event_if_there_is_article_associated(self):
        self.assertEqual(InstitutionType.objects.count(), 0)
        self.assertEqual(Institution.objects.count(), 0)
        self.assertEqual(Event.objects.count(), 0)
        self.assertEqual(Article.objects.count(), 0)

        institution_type = InstitutionType.objects.create(name='Institution_Type_Test')
        institution = Institution.objects.create(name='Institution_Test', type=institution_type)

        event = Event.objects.create(
            name='Event_Test',
            publisher=institution,
            start_date=timezone.now(),
            end_date=timezone.now(),
            local='Algum Lugar, Planeta Terra'
        )

        article = Article.objects.create(
            team='s',
            title='Article_Test',
            research_result_type='a',
            event=event,
            status='Status_Test'
        )

        with self.assertRaises(ProtectedError) as e:
            event.delete()

        self.assertEqual(InstitutionType.objects.last(), institution_type)
        self.assertEqual(Institution.objects.last(), institution)
        self.assertEqual(Event.objects.last(), event)
        self.assertEqual(Article.objects.last(), article)
        self.assertEqual(Article.objects.last().event, event)

    def test_do_not_delete_type_academic_work_if_there_is_academic_work_associated(self):
        self.assertEqual(Person.objects.count(), 0)
        self.assertEqual(TypeAcademicWork.objects.count(), 0)
        self.assertEqual(AcademicWork.objects.count(), 0)

        person = Person.objects.create(full_name='Person_Test')
        type_academic_work = TypeAcademicWork.objects.create(name='Type_Academic_Work_Test')

        academic_work = AcademicWork.objects.create(
            type=type_academic_work,
            title='Academic_Work_Test',
            advisee=person,
            advisor=person,
            funding=True,
            funding_agency='Funding_Agency_Test',
            start_date=timezone.now(),
            abstract='Abstract_Test'
        )

        with self.assertRaises(ProtectedError) as e:
            type_academic_work.delete()

        self.assertEqual(Person.objects.last(), person)
        self.assertEqual(TypeAcademicWork.objects.last(), type_academic_work)
        self.assertEqual(AcademicWork.objects.last(), academic_work)
        self.assertEqual(AcademicWork.objects.last().type, type_academic_work)

    def test_do_not_delete_person_if_there_is_academic_work_associated(self):
        self.assertEqual(Person.objects.count(), 0)
        self.assertEqual(TypeAcademicWork.objects.count(), 0)
        self.assertEqual(AcademicWork.objects.count(), 0)

        person = Person.objects.create(full_name='Person_Test')
        type_academic_work = TypeAcademicWork.objects.create(name='Type_Academic_Work_Test')

        academic_work = AcademicWork.objects.create(
            type=type_academic_work,
            title='Academic_Work_Test',
            advisee=person,
            advisor=person,
            funding=True,
            funding_agency='Funding_Agency_Test',
            start_date=timezone.now(),
            abstract='Abstract_Test'
        )

        with self.assertRaises(ProtectedError) as e:
            person.delete()

        self.assertEqual(Person.objects.last(), person)
        self.assertEqual(TypeAcademicWork.objects.last(), type_academic_work)
        self.assertEqual(AcademicWork.objects.last(), academic_work)
        self.assertEqual(AcademicWork.objects.last().type, type_academic_work)

    def test_delete_author_instance_associated_with_research_result_when_this_one_is_deleted(self):
        self.assertEqual(Person.objects.count(), 0)
        self.assertEqual(Author.objects.count(), 0)
        self.assertEqual(ResearchResult.objects.count(), 0)

        person = Person.objects.create(full_name='Person_Test')

        research_result = ResearchResult.objects.create(
            team='s',
            title='Research_Result',
            research_result_type='a')

        author = Author.objects.create(author=person, research_result=research_result, order=1)

        research_result.person.add(person)
        research_result.save()

        self.assertEqual(Person.objects.last(), person)
        self.assertEqual(Author.objects.last(), author)
        self.assertEqual(ResearchResult.objects.last(), research_result)

        research_result.delete()

        self.assertEqual(Person.objects.count(), 1)
        self.assertEqual(Author.objects.count(), 0)
        self.assertEqual(ResearchResult.objects.count(), 0)

    def test_delete_periodical_rsi_file_instance_associated_with_periodical_when_this_one_is_deleted(self):
        self.assertEqual(Periodical.objects.count(), 0)
        self.assertEqual(PeriodicalRISFile.objects.count(), 0)

        periodical = Periodical.objects.create(name='Periodical_Test')
        periodical_rsi_file = PeriodicalRISFile.objects.create(periodical=periodical, name='Periodical_RSI_File_Test')

        self.assertEqual(Periodical.objects.last(), periodical)
        self.assertEqual(PeriodicalRISFile.objects.last(), periodical_rsi_file)

        periodical.delete()

        self.assertEqual(Periodical.objects.count(), 0)
        self.assertEqual(PeriodicalRISFile.objects.count(), 0)

    def test_delete_event_rsi_file_instance_associated_with_event_when_this_one_is_deleted(self):
        self.assertEqual(Event.objects.count(), 0)
        self.assertEqual(EventRISFile.objects.count(), 0)

        event = Event.objects.create(
            name='Event_Test',
            start_date=timezone.now(),
            end_date=timezone.now(),
            local='Algum Lugar, Planeta Terra'
        )

        event_rsi_file = EventRISFile.objects.create(event=event, name='Event_RSI_File_Test')

        self.assertEqual(Event.objects.last(), event)
        self.assertEqual(EventRISFile.objects.last(), event_rsi_file)

        event.delete()

        self.assertEqual(Event.objects.count(), 0)
        self.assertEqual(EventRISFile.objects.count(), 0)

    def test_delete_draft_instance_associated_with_article_when_this_one_is_deleted(self):
        self.assertEqual(Article.objects.count(), 0)
        self.assertEqual(Draft.objects.count(), 0)

        article = Article.objects.create(
            team='s',
            title='Article_Test',
            research_result_type='a',
            status='Status_Test'
        )

        draft = Draft.objects.create(article=article, date=timezone.now())

        self.assertEqual(Article.objects.last(), article)
        self.assertEqual(Draft.objects.last(), draft)

        article.delete()

        self.assertEqual(Article.objects.count(), 0)
        self.assertEqual(Draft.objects.count(), 0)

    def test_delete_submitted_instance_associated_with_article_when_this_one_is_deleted(self):
        self.assertEqual(Article.objects.count(), 0)
        self.assertEqual(Submitted.objects.count(), 0)

        article = Article.objects.create(
            team='s',
            title='Article_Test',
            research_result_type='a',
            status='Status_Test'
        )

        submitted = Submitted.objects.create(article=article, date=timezone.now())

        self.assertEqual(Article.objects.last(), article)
        self.assertEqual(Submitted.objects.last(), submitted)

        article.delete()

        self.assertEqual(Article.objects.count(), 0)
        self.assertEqual(Submitted.objects.count(), 0)

    def test_delete_accepted_instance_associated_with_article_when_this_one_is_deleted(self):
        self.assertEqual(Article.objects.count(), 0)
        self.assertEqual(Accepted.objects.count(), 0)

        article = Article.objects.create(
            team='s',
            title='Article_Test',
            research_result_type='a',
            status='Status_Test'
        )

        accepted = Accepted.objects.create(article=article, date=timezone.now())

        self.assertEqual(Article.objects.last(), article)
        self.assertEqual(Accepted.objects.last(), accepted)

        article.delete()

        self.assertEqual(Article.objects.count(), 0)
        self.assertEqual(Accepted.objects.count(), 0)

    def test_delete_published_instance_associated_with_article_when_this_one_is_deleted(self):
        self.assertEqual(Article.objects.count(), 0)
        self.assertEqual(Published.objects.count(), 0)

        article = Article.objects.create(
            team='s',
            title='Article_Test',
            research_result_type='a',
            status='Status_Test'
        )

        published = Published.objects.create(article=article)

        self.assertEqual(Article.objects.last(), article)
        self.assertEqual(Published.objects.last(), published)

        article.delete()

        self.assertEqual(Article.objects.count(), 0)
        self.assertEqual(Published.objects.count(), 0)
