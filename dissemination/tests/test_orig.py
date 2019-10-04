# -*- coding: utf-8 -*-
from django.urls import reverse
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from dissemination.models import InternalMediaOutlet, Internal, ExternalMediaOutlet, External
from research.tests.test_orig import system_authentication


class DisseminationTest(TestCase):

    """
    The following tests are performed:
    1 - Dissemination report for external with date;
    2 - Dissemination report for external without date;
    3 - Dissemination report for internal with date;
    4 - Dissemination report for internal without date;
    5 - Dissemination report without type selected;
    6 - Dissemination report with invalid dates selected.
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

    def test_dissemination_report_without_date(self):

        # With type external selected
        response = self.client.post(reverse('dissemination_report'), {'type': 'e', 'start_date': '', 'end_date': ''})
        cont = response.context['disseminations']
        self.assertEqual(len(cont), 1)
        self.assertEqual(response.status_code, 200)

        # With type internal selected
        internal_types = InternalMediaOutlet.objects.all()
        internal_types = [{'value': media.id, 'display': media.name} for media in internal_types]

        for media in internal_types:
            value = media['value']
            response = self.client.post(reverse('dissemination_report'), {'type': 'i',
                                                                          'internal_type': value,
                                                                          'start_date': '',
                                                                          'end_date': ''})
            cont = response.context['disseminations']
            self.assertEqual(len(cont), 1)
            self.assertEqual(response.status_code, 200)

        self.assertEqual(response.status_code, 200)

    def test_dissemination_report_with_date_and_internal_media_type(self):
        internal_types = InternalMediaOutlet.objects.all()
        internal_types = [{'value': media.id, 'display': media.name} for media in internal_types]

        for media in internal_types:
            value = media['value']
            response = self.client.post(reverse('dissemination_report'), {'type': 'i',
                                                                          'internal_type': value,
                                                                          'start_date': '01/01/2015',
                                                                          'end_date': '03/05/2017'})
            cont = response.context['disseminations']
            self.assertEqual(len(cont), 1)
            self.assertEqual(response.status_code, 200)

    def test_dissemination_report_with_date_and_external_media_type(self):
        # With type external selected
        response = self.client.post(reverse('dissemination_report'), {'type': 'e',
                                                                      'start_date': '01/01/2015',
                                                                      'end_date': '01/02/2017'})
        cont = response.context['disseminations']
        self.assertEqual(len(cont), 1)
        self.assertEqual(response.status_code, 200)

    def test_dissemination_report_with_date_in_wrong_format_and_media_type_0_raises_message_error(self):
        response = self.client.post(reverse('dissemination_report'), {'type': '0',
                                                                      'start_date': '2015/01/01',
                                                                      'end_date': '2017/01/02'})
        for message in response.context['messages']:
            self.assertEqual(message.message, _('You should choose a type.'))

    def test_dissemination_report_with_date_in_wrong_format_and_media_type_different_from_0_raises_message_error(self):
        response = self.client.post(reverse('dissemination_report'), {'type': 'e',
                                                                      'start_date': '2015/01/01',
                                                                      'end_date': '2017/01/02'})
        for message in response.context['messages']:
            self.assertEqual(message.message, _('You entered a wrong date format or the end date is not greater '
                                                'than or equal to the start date.'))

    def test_without_type(self):
        response = self.client.get(reverse('dissemination_report'))
        self.assertEqual(response.status_code, 200)

    def test_dissemination_report_invalid_dates(self):
        # With type external selected
        response = self.client.post(reverse('dissemination_report'), {'type': 'e',
                                                                      'start_date': '01/01/2019',
                                                                      'end_date': '01/02/2017'})
        self.assertEqual(response.status_code, 200)

    def test_dissemination_file_external_media_type_and_tex_extension_generates_latex(self):
        start_date = '2015-01-01'
        end_date = '2017-01-01'
        filename = 'filename'
        extension = '.tex'

        response = self.client.get(reverse('dissemination_file'), {'type': 'e',
                                                                   'start_date': start_date,
                                                                   'end_date': end_date,
                                                                   'filename': filename,
                                                                   'extension': extension})
        cont = response.context['disseminations']
        self.assertEqual(len(cont), 1)
        self.assertTemplateUsed(response, 'report/dissemination/tex/disseminations.tex')

    def test_dissemination_file_internal_media_type_and_tex_extension_generates_latex(self):
        start_date = '2015-01-01'
        end_date = '2017-01-01'
        filename = 'filename'
        extension = '.tex'

        internal_types = InternalMediaOutlet.objects.all()
        internal_types = [{'value': media.id, 'display': media.name} for media in internal_types]

        for media in internal_types:
            value = media['value']
            response = self.client.get(reverse('dissemination_file'), {'type': 'i',
                                                                       'start_date': start_date,
                                                                       'end_date': end_date,
                                                                       'filename': filename,
                                                                       'extension': extension,
                                                                       'internal_type': value})
            cont = response.context['disseminations']
            self.assertEqual(len(cont), 1)
            self.assertTemplateUsed(response, 'report/dissemination/tex/disseminations.tex')

    def test_dissemination_file_external_media_type_and_pdf_extension_generates_latex(self):
        start_date = '2015-01-01'
        end_date = '2017-01-01'
        filename = 'filename'
        extension = '.pdf'

        response = self.client.get(reverse('dissemination_file'), {'type': 'e',
                                                                   'start_date': start_date,
                                                                   'end_date': end_date,
                                                                   'filename': filename,
                                                                   'extension': extension})
        cont = response.context['disseminations']
        self.assertEqual(len(cont), 1)
        self.assertTemplateUsed(response, 'report/dissemination/pdf/dissemination.html')

    def test_dissemination_file_internal_media_type_and_pdf_extension_generates_latex(self):
        start_date = '2015-01-01'
        end_date = '2017-01-01'
        filename = 'filename'
        extension = '.pdf'

        internal_types = InternalMediaOutlet.objects.all()
        internal_types = [{'value': media.id, 'display': media.name} for media in internal_types]

        for media in internal_types:
            value = media['value']
            response = self.client.get(reverse('dissemination_file'), {'type': 'i',
                                                                       'start_date': start_date,
                                                                       'end_date': end_date,
                                                                       'filename': filename,
                                                                       'extension': extension,
                                                                       'internal_type': value})
            cont = response.context['disseminations']
            self.assertEqual(len(cont), 1)
            self.assertTemplateUsed(response, 'report/dissemination/pdf/dissemination.html')
