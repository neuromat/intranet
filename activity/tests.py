import datetime
from activity.models import Seminar,SeminarType, TrainingProgram
from activity.views import render_to_pdf, training_programs_search, seminars_search
from django.core.urlresolvers import reverse
from django.db.models.query import QuerySet
from django.test import TestCase
from person.models import Person
from research.tests import system_authentication


def seminar(title, seminar_type, date):
    return Seminar(title=title,  type_of_activity='s', category=seminar_type, date=date)


def training_program(title, start_date):
    return TrainingProgram(title=title, start_date=start_date)


class TrainingProgramTest(TestCase):

    def setUp(self):
        logged, self.user, self.factory = system_authentication(self)
        self.assertEqual(logged, True)

        self.date1 = datetime.date(2015, 1, 16)
        self.date2 = datetime.date(2014, 1, 16)

        training1 = training_program("Test 1", self.date1)
        training1.save()

        training2 = training_program("Test 2", self.date2)
        training2.save()

    def test_search(self):
        response = training_programs_search(self.date2, self.date1)
        self.assertTrue(isinstance(response, QuerySet))

    def test_tex(self):
        response = self.client.get(reverse('training_programs_latex'), {'start_date': '2015-03-01',
                                                                        'end_date': '2017-03-05'})
        self.assertEqual(response.status_code, 200)

    def test_report(self):

        # With nothing
        response = self.client.get(reverse('training_programs_report'))
        self.assertEqual(response.status_code, 200)

        # With date
        response = self.client.post(reverse('training_programs_report'), {'start_date': '01-01-2015',
                                                                          'end_date': '03-05-2017'})
        cont = response.context['training_programs']
        self.assertEqual(len(cont), 1)
        self.assertEqual(response.status_code, 200)

        # Without date
        response = self.client.post(reverse('training_programs_report'), {'start_date': '01-01-2014',
                                                                          'end_date': '03-05-2017'})
        cont = response.context['training_programs']
        self.assertEqual(len(cont), 2)
        self.assertEqual(response.status_code, 200)

        # With wrong date
        response = self.client.post(reverse('training_programs_report'), {'start_date': '01-01-2017',
                                                                          'end_date': '03-05-2015'})
        self.assertEqual(response.status_code, 200)


class SeminarsTest(TestCase):

    def setUp(self):
        logged, self.user, self.factory = system_authentication(self)
        self.assertEqual(logged, True)

        person = Person(full_name="Person Full Test")
        person.save()

        type1 = SeminarType(name="Testing 1")
        type1.save()

        type2 = SeminarType(name="Testing 2")
        type2.save()

        self.date1 = datetime.date(2015, 1, 16)
        self.date2 = datetime.date(2014, 1, 16)

        seminar1 = seminar('Seminar1', type1, self.date1)
        seminar1.save()

        seminar2 = seminar('Seminar2', type2, self.date2)
        seminar2.save()

    def test_report(self):

        # With nothing
        response = self.client.get(reverse('seminars_report'))
        self.assertEqual(response.status_code, 200)

        # With date and all categories
        response = self.client.post(reverse('seminars_report'), {'start_date': '01-01-2015',
                                                                 'end_date': '03-05-2017',
                                                                 'category': '0'})
        cont = response.context['seminars']
        self.assertEqual(len(cont), 1)
        self.assertEqual(response.status_code, 200)

        # With date and specific category
        response = self.client.post(reverse('seminars_report'), {'start_date': '01-01-2015',
                                                                 'end_date': '03-05-2017',
                                                                 'category': 'All'})
        cont = response.context['seminars']
        self.assertEqual(len(cont), 1)
        self.assertEqual(response.status_code, 200)

        # Without date
        response = self.client.post(reverse('seminars_report'), {'start_date': '',
                                                                 'end_date': '',
                                                                 'category': '0'})
        cont = response.context['seminars']
        self.assertEqual(len(cont), 2)
        self.assertEqual(response.status_code, 200)

        # Wrong dates
        response = self.client.post(reverse('seminars_report'), {'start_date': '01-01-2016',
                                                                 'end_date': '03-05-2015',
                                                                 'category': 'All'})
        self.assertEqual(response.status_code, 200)

    def test_poster(self):

        # Just load the page
        response = self.client.get(reverse('seminar_poster'))
        self.assertEqual(response.status_code, 200)

        # Test creation of seminar poster..
        response = self.client.post(reverse('seminar_poster'), {'title': ''})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('seminar_poster'), {'title': 0})
        self.assertEqual(response.status_code, 404)

        response = self.client.post(reverse('seminar_poster'), {'title': 1})
        self.assertEqual(response.status_code, 200)

    def test_tex(self):
        response = self.client.get(reverse('seminar_latex'), {'start_date': '2015-03-01',
                                                              'end_date': '2017-03-05',
                                                              'category': 'All'})
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        response = seminars_search(self.date2, self.date1, 'All')
        self.assertTrue(isinstance(response, QuerySet))

        response = seminars_search(self.date2, self.date1, 0)
        self.assertTrue(isinstance(response, QuerySet))

    def test_titles(self):
        response = self.client.get(reverse('seminar_show_titles'), {'speaker': 1})
        self.assertEqual(response.status_code, 404)  # Expected failure, because we need to assign a person to seminar!
