import datetime
from activity.models import Seminar,SeminarType
from django.core.urlresolvers import reverse
from django.test import TestCase
from research.tests import system_authentication


def seminar(title, seminar_type, date):
    return Seminar(title=title, type_of_activity='s', category=seminar_type, date=date)


class ActivityTest(TestCase):

    def setUp(self):
        logged, self.user, self.factory = system_authentication(self)
        self.assertEqual(logged, True)

        # person = Person(full_name="Person Full Test")
        # person.save()

        type1 = SeminarType(name="Testing 1")
        type1.save()

        type2 = SeminarType(name="Testing 2")
        type2.save()

        date1 = datetime.date(2015, 1, 16)
        date2 = datetime.date(2014, 1, 16)

        seminar1 = seminar('Seminar1', type1, date1)
        seminar1.save()

        seminar2 = seminar('Seminar2', type2, date2)
        seminar2.save()

    def test_seminar(self):

        # With nothing
        response = self.client.get(reverse('seminars_report'))
        self.assertEqual(response.status_code, 200)

        # With date and all categories
        response = self.client.post(reverse('seminars_report'), {'start_date': '01-01-2015',
                                                                 'end_date': '03-05-2017',
                                                                 'category': 'All'})
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
                                                                 'category': 'All'})
        cont = response.context['seminars']
        self.assertEqual(len(cont), 2)
        self.assertEqual(response.status_code, 200)

        # Wrong dates
        response = self.client.post(reverse('seminars_report'), {'start_date': '01-01-2016',
                                                                 'end_date': '03-05-2015',
                                                                 'category': 'All'})
        self.assertEqual(response.status_code, 200)

    def test_tex(self):
        response = self.client.get(reverse('seminar_latex'), {'start_date': '2015-03-01',
                                                              'end_date': '2017-03-05',
                                                              'category': 'All'})
        self.assertEqual(response.status_code, 200)
