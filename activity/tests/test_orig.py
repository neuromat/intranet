import datetime

from django.urls import reverse
from django.db.models.query import QuerySet
from django.test import TestCase

from activity.models import Seminar, SeminarType, TrainingProgram, Meeting
from activity.views import training_programs_search, seminars_search
from person.models import Person
from research.tests.test_orig import system_authentication

# DRY with dates
base_date1 = datetime.date(2015, 1, 16)
base_date2 = datetime.date(2014, 1, 16)
base_date3 = datetime.date(2014, 1, 17)


def seminar(title, seminar_type, date):
    return Seminar(title=title,  type_of_activity='s', category=seminar_type, date=date)


def training_program(title, start_date):
    return TrainingProgram(title=title, start_date=start_date)


def meeting(title, start_date, end_date, broad_audience):
    return Meeting(title=title, start_date=start_date, end_date=end_date, broad_audience=broad_audience)


class TrainingProgramTest(TestCase):

    """
    The following tests are performed:
    1 - Training programs search;
    2 - Training programs report in .tex;
    3 - Training programs report with date;
    4 - Training programs report without date;
    5 - Training programs report with invalid date.
    6 - Training programs report in .pdf;
    """

    def setUp(self):
        logged, self.user, self.factory = system_authentication(self)
        self.assertEqual(logged, True)

        self.date1 = base_date1
        self.date2 = base_date2

        training1 = training_program("Test 1", self.date1)
        training1.save()

        training2 = training_program("Test 2", self.date2)
        training2.save()

    def test_search(self):
        response = training_programs_search(self.date2, self.date1)
        self.assertTrue(isinstance(response, QuerySet))

    def test_tex(self):
        response = self.client.get(reverse('training_programs_file'), {'start_date': '2015-03-01',
                                                                       'end_date': '2017-03-05',
                                                                       'extension': '.tex'})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('training_programs_file'), {'start_date': '2015-03-01',
                                                                       'end_date': '2017-03-05',
                                                                       'extension': '.pdf'})
        self.assertEqual(response.status_code, 200)

    def test_report_status_code(self):
        response = self.client.get(reverse('training_programs_report'))
        self.assertEqual(response.status_code, 200)

    def test_report_with_date(self):
        response = self.client.post(reverse('training_programs_report'), {'start_date': '01/01/2015',
                                                                          'end_date': '03/05/2017'})
        cont = response.context['training_programs']
        self.assertEqual(len(cont), 1)
        self.assertEqual(response.status_code, 200)

    def test_report_without_date(self):
        response = self.client.post(reverse('training_programs_report'), {'start_date': '',
                                                                          'end_date': ''})
        cont = response.context['training_programs']
        self.assertEqual(len(cont), 2)
        self.assertEqual(response.status_code, 200)

    def test_report_with_wrong_date(self):
        response = self.client.post(reverse('training_programs_report'), {'start_date': '01/01/2017',
                                                                          'end_date': '03/05/2015'})
        self.assertEqual(response.status_code, 200)


class SeminarsTest(TestCase):

    """
    The following tests are performed:
    1 - Seminars search;
    2 - Seminars report in latex and pdf;
    3 - Seminars report for internal with date;
    4 - Seminars report  without date;
    5 - Seminars report with invalid dates selected;
    6 - Seminars poster.
    """

    def setUp(self):
        logged, self.user, self.factory = system_authentication(self)
        self.assertEqual(logged, True)

        self.person = Person(full_name="Person Full Test")
        self.person.save()

        type1 = SeminarType(name="Testing 1")
        type1.save()

        type2 = SeminarType(name="Testing 2")
        type2.save()

        self.date1 = base_date1
        self.date2 = base_date2

        seminar1 = seminar('Seminar1', type1, self.date1)
        seminar1.save()

        seminar2 = seminar('Seminar2', type2, self.date2)
        seminar2.save()

    def test_report_status_code(self):
        response = self.client.get(reverse('seminars_report'))
        self.assertEqual(response.status_code, 200)

    def test_report_with_dates_and_all_categories(self):

        response = self.client.post(reverse('seminars_report'), {'start_date': '01/01/2015',
                                                                 'end_date': '03/05/2017',
                                                                 'category': '0'})
        cont = response.context['seminars']
        self.assertEqual(len(cont), 1)
        self.assertEqual(response.status_code, 200)

    def test_report_with_dates_and_specific_category(self):
        response = self.client.post(reverse('seminars_report'), {'start_date': '01/01/2015',
                                                                 'end_date': '03/05/2017',
                                                                 'category': 'All'})
        cont = response.context['seminars']
        self.assertEqual(len(cont), 1)
        self.assertEqual(response.status_code, 200)

    def test_report_without_dates(self):
        response = self.client.post(reverse('seminars_report'), {'start_date': '',
                                                                 'end_date': '',
                                                                 'category': '0'})
        cont = response.context['seminars']
        self.assertEqual(len(cont), 2)
        self.assertEqual(response.status_code, 200)

    def test_report_with_wrong_dates(self):
        response = self.client.post(reverse('seminars_report'), {'start_date': '01/01/2016',
                                                                 'end_date': '03/05/2015',
                                                                 'category': 'All'})
        self.assertEqual(response.status_code, 200)

    def test_poster(self):

        # Just load the page
        response = self.client.get(reverse('seminars_poster'))
        self.assertEqual(response.status_code, 200)

        # Test creation of seminar poster..
        response = self.client.post(reverse('seminars_poster'), {'title': ''})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('seminars_poster'), {'title': 0})
        self.assertEqual(response.status_code, 404)

        # seminar_id = Seminar.objects.get(title='Seminar1')
        # seminar_id = seminar_id.pk
        #
        # response = self.client.post(reverse('seminars_poster'), {'title': seminar_id})
        # self.assertEqual(response.status_code, 200)

    def test_tex(self):
        response = self.client.get(reverse('seminars_file'), {'start_date': '2015-03-01',
                                                              'end_date': '2017-03-05',
                                                              'category': 'All',
                                                              'extension': '.tex'})
        self.assertEqual(response.status_code, 200)

    def test_pdf(self):
        response = self.client.get(reverse('seminars_file'), {'start_date': '2015-03-01',
                                                              'end_date': '2017-03-05',
                                                              'category': 'All',
                                                              'extension': '.pdf'})
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        response = seminars_search(self.date2, self.date1, 'All')
        self.assertTrue(isinstance(response, QuerySet))

        response = seminars_search(self.date2, self.date1, 0)
        self.assertTrue(isinstance(response, QuerySet))

    def test_titles(self):

        speaker = self.person.pk
        response = self.client.get(reverse('seminars_show_titles'), {'speaker': speaker})
        self.assertEqual(response.status_code, 200)


class MeetingsTest(TestCase):

    """
    The following tests are performed:
    1 - Meetings report with date for each audience;
    2 - Meetings report without date;
    3 - Meetings report with invalid date.
    """

    def setUp(self):

        logged, self.user, self.factory = system_authentication(self)
        self.assertEqual(logged, True)

        self.person = Person(full_name="Person Full Test")
        self.person.save()

        self.date1 = base_date2
        self.date2 = base_date1
        self.date3 = base_date3

        meeting1 = meeting('First meeting', self.date1, self.date2, False)
        meeting1.save()

        meeting2 = meeting('Second meeting', self.date1, self.date3, True)
        meeting2.save()

        meeting3 = meeting('Third meeting', self.date1, self.date3, True)
        meeting3.save()

    def test_report_status_code(self):
        response = self.client.get(reverse('meetings_report'))
        self.assertEqual(response.status_code, 200)

    def test_report_with_valid_date(self):
        # With valid date, to each audience
        response = self.client.post(reverse('meetings_report'), {'start_date': '01/01/2014',
                                                                 'end_date': '03/05/2017',
                                                                 'broad_audience': 0})
        cont = response.context['meetings']
        self.assertEqual(len(cont), 3)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('meetings_report'), {'start_date': '01/01/2014',
                                                                 'end_date': '03/05/2017',
                                                                 'broad_audience': 1})
        cont = response.context['meetings']
        self.assertEqual(len(cont), 2)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('meetings_report'), {'start_date': '01/01/2014',
                                                                 'end_date': '03/05/2015',
                                                                 'broad_audience': 2})
        cont = response.context['meetings']
        self.assertEqual(len(cont), 1)
        self.assertEqual(response.status_code, 200)

    def test_report_without_date(self):
        # Without date, all categories. Should get all results.
        response = self.client.post(reverse('meetings_report'), {'start_date': '',
                                                                 'end_date': '',
                                                                 'broad_audience': 0})
        cont = response.context['meetings']
        self.assertEqual(len(cont), 3)
        self.assertEqual(response.status_code, 200)

    def test_report_wrong_date(self):
        response = self.client.post(reverse('meetings_report'), {'start_date': '01/01/2017',
                                                                 'end_date': '03/05/2015'})
        self.assertEqual(response.status_code, 200)
