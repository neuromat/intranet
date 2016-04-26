# -*- coding: utf-8 -*-
from dissemination.views import dissemination_report
from research.tests import system_authentication
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory


class DisseminationTest(TestCase):

    def setUp(self):
        logged, self.user, self.factory = system_authentication(self)
        self.assertEqual(logged, True)

    def test_without_type(self):
        response = self.client.get(reverse('dissemination_report'))
        self.assertEqual(response.status_code, 200)

    def test_dissemination_report_without_date (self):

        # With type external selected
        request = self.factory.post(reverse('dissemination_report'), {'type': 'e',
                                                                      'start_date': '',
                                                                      'end_date': ''})
        request.user = self.user
        response = dissemination_report(request)
        self.assertEqual(response.status_code, 200)

        # With type internal selected
        request = self.factory.post(reverse('dissemination_report'), {'type': 'i',
                                                                      'internal_type': 1,
                                                                      'start_date': '',
                                                                      'end_date': ''})
        request.user = self.user
        response = dissemination_report(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.post(reverse('dissemination_report'), {'type': 'i',
                                                                      'internal_type': 2,
                                                                      'start_date': '',
                                                                      'end_date': ''})
        request.user = self.user
        response = dissemination_report(request)
        self.assertEqual(response.status_code, 200)

    def test_dissemination_report_with_date (self):

        # With type external selected
        request = self.factory.post(reverse('dissemination_report'), {'type': 'e',
                                                                      'start_date': '01-01-2015',
                                                                      'end_date': '01-02-2015'})
        request.user = self.user
        response = dissemination_report(request)
        self.assertEqual(response.status_code, 200)

        # With type internal selected
        request = self.factory.post(reverse('dissemination_report'), {'type': 'i',
                                                                      'internal_type': 1,
                                                                      'start_date': '01-02-2015',
                                                                      'end_date': '03-05-2015'})
        request.user = self.user
        response = dissemination_report(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.post(reverse('dissemination_report'), {'type': 'i',
                                                                      'internal_type': 2,
                                                                      'start_date': '01-06-2015',
                                                                      'end_date': '10-07-2015'})
        request.user = self.user
        response = dissemination_report(request)
        self.assertEqual(response.status_code, 200)

