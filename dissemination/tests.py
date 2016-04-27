# -*- coding: utf-8 -*-
from dissemination.models import InternalMediaOutlet, Internal, ExternalMediaOutlet, External
from research.tests import system_authentication
from django.core.urlresolvers import reverse
from django.test import TestCase


class DisseminationTest(TestCase):

    """
    The following tests are performed:
    1 - Dissemination report for external with date;
    2 - Dissemination report for external without date;
    3 - Dissemination report for internal with date;
    4 - Dissemination report for internal without date;
    5 - Dissemination report without type selected.
    """

    def setUp(self):

        logged, self.user, self.factory = system_authentication(self)
        self.assertEqual(logged, True)

        internal_media_1 = InternalMediaOutlet(name="Blog")
        internal_media_1.save()

        internal_media_2 = InternalMediaOutlet(name="Newsletter")
        internal_media_2.save()

        dissemination1 = Internal(title='Hello, blog!', date='2015-01-01', media_outlet=internal_media_1)
        dissemination1.save()

        dissemination2 = Internal(title='Hello, newsletter!', date='2015-01-02', media_outlet=internal_media_2)
        dissemination2.save()

        external_media = ExternalMediaOutlet(name='External Blog')
        external_media.save()

        dissemination3 = External(title='Hello, external blog!', date='2015-01-03', media_outlet=external_media)
        dissemination3.save()

    def test_dissemination_report_without_date (self):

        # With type external selected
        response = self.client.post(reverse('dissemination_report'), {'type': 'e',
                                                                     'start_date': '',
                                                                     'end_date': ''})
        cont = response.context['disseminations']
        self.assertEqual(len(cont), 1)
        self.assertEqual(response.status_code, 200)

        # With type internal selected
        internal_types = InternalMediaOutlet.objects.all()
        internal_types = [{'value': type.id, 'display': type.name} for type in internal_types]

        for type in internal_types:
            value = type['value']
            response = self.client.post(reverse('dissemination_report'), {'type': 'i',
                                                                          'internal_type': value,
                                                                          'start_date': '',
                                                                          'end_date': ''})
            cont = response.context['disseminations']
            self.assertEqual(len(cont), 1)
            self.assertEqual(response.status_code, 200)

        self.assertEqual(response.status_code, 200)

    def test_dissemination_report_with_date (self):

        # With type external selected
        response = self.client.post(reverse('dissemination_report'), {'type': 'e',
                                                                      'start_date': '01-01-2015',
                                                                      'end_date': '01-02-2017'})
        cont = response.context['disseminations']
        self.assertEqual(len(cont), 1)
        self.assertEqual(response.status_code, 200)

        # With type internal selected
        internal_types = InternalMediaOutlet.objects.all()
        internal_types = [{'value': type.id, 'display': type.name} for type in internal_types]

        for type in internal_types:
            value = type['value']
            response = self.client.post(reverse('dissemination_report'), {'type': 'i',
                                                                          'internal_type': value,
                                                                          'start_date': '01-01-2015',
                                                                          'end_date': '03-05-2017'})
            cont = response.context['disseminations']
            self.assertEqual(len(cont), 1)
            self.assertEqual(response.status_code, 200)

    def test_without_type(self):
        response = self.client.get(reverse('dissemination_report'))
        self.assertEqual(response.status_code, 200)
