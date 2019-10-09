import datetime
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.forms.models import inlineformset_factory

from cities_light.models import City, Region, Country
from scientific_mission.models import ScientificMission, Route
from person.models import Person
from configuration.models import PrincipalInvestigator, ProcessNumber

from scientific_mission.admin import InlineValidationDate

from research.tests.test_orig import system_authentication
from scientific_mission.views import get_missions


# Create a scientific mission for testing
def scientific_mission(person, amount_paid):
    return ScientificMission(person=person, amount_paid=amount_paid)


# Create routes
def create_route(city, mission, date_time, order):
    return Route(scientific_mission=mission, origin_city=city, destination_city=city, departure=date_time,
                 arrival=date_time, order=order)


class ScientificMissionsTest(TestCase):

    """
    The following tests are performed:
    1 - Scientific Missions report with date;
    2 - Scientific Missions report without date;
    3 - Load Origin Cities;
    4 - Load Destination Cities;
    5 - Anexo 5 and its conditionals.
    """

    def setUp(self):
        logged, self.user, self.factory = system_authentication(self)
        self.assertEqual(logged, True)

        country, created = Country.objects.get_or_create(name_ascii='Brazil', slug='brazil')

        city, created = City.objects.get_or_create(country=country, name_ascii='Sao Paulo', slug='sao-paulo')

        person = Person(full_name="Fulano Testeiro")
        person.save()

        date_departure1 = timezone.now() - timezone.timedelta(1)
        date_arrival1 = timezone.now()

        date_departure2 = timezone.now() - timezone.timedelta(366)
        date_arrival2 = timezone.now() - timezone.timedelta(365)
        order_01 = 0
        order_02 = 1

        amount_paid = 666

        mission1 = scientific_mission(person, amount_paid)
        mission1.save()
        route1_mission1 = create_route(city, mission1, date_departure1, order_01)
        route2_mission1 = create_route(city, mission1, date_arrival1, order_02)
        route1_mission1.save()
        route2_mission1.save()

        mission2 = scientific_mission(person, amount_paid)
        mission2.save()
        route1_mission2 = create_route(city, mission2, date_departure2, order_01)
        route2_mission2 = create_route(city, mission2, date_arrival2, order_02)
        route1_mission2.save()
        route2_mission2.save()

    def test_report(self):

        # With nothing
        response = self.client.get(reverse('missions_report'))
        self.assertEqual(response.status_code, 200)

        start_date = timezone.now() - timezone.timedelta(363)
        start_date_str = str(start_date.day) + '/' + str(start_date.month) + '/' + str(start_date.year)
        end_date = timezone.now() + timezone.timedelta(363)
        end_date_str = str(end_date.day) + '/' + str(end_date.month) + '/' + str(end_date.year)

        # With date
        response = self.client.post(reverse('missions_report'),
                                    {'start_date': start_date_str, 'end_date': end_date_str})
        cont = response.context['missions']
        self.assertEqual(len(cont), 1)
        self.assertEqual(response.status_code, 200)

        end_date_2 = timezone.now() + timezone.timedelta(363)
        end_date_str_2 = str(end_date_2.day) + '/' + str(end_date_2.month) + '/' + str(end_date_2.year)

        # With date, but out of range
        response = self.client.post(reverse('missions_report'), {'start_date': end_date_str,
                                                                 'end_date': end_date_str_2})
        cont = response.context['missions']
        self.assertEqual(len(cont), 0)
        self.assertEqual(response.status_code, 200)

        # Without date
        response = self.client.post(reverse('missions_report'), {'start_date': '',
                                                                 'end_date': ''})
        cont = response.context['missions']
        self.assertEqual(len(cont), 2)
        self.assertEqual(response.status_code, 200)

        # Wrong dates
        response = self.client.post(reverse('missions_report'), {'start_date': end_date_str_2,
                                                                 'end_date': end_date_str})
        self.assertEqual(response.status_code, 200)

    def test_tex(self):
        start_date = timezone.now() - timezone.timedelta(363)
        start_date_str = str(start_date.year) + '-' + str(start_date.month) + '-' + str(start_date.day)
        end_date = timezone.now() + timezone.timedelta(363)
        end_date_str = str(end_date.year) + '-' + str(end_date.month) + '-' + str(end_date.day)

        response = self.client.get(reverse('scientific_missions_file'), {'start_date': start_date_str,
                                                                         'end_date': end_date_str,
                                                                         'extension': '.tex'})
        cont = response.context['missions']
        self.assertEqual(len(cont), 1)
        self.assertEqual(response.status_code, 200)

    def test_city_auto_complete_passing_q_argument(self):
        country = Country.objects.create(name='Brazil', name_ascii='Brazil', slug='brazil')
        region = Region.objects.create(name='São Paulo', name_ascii='Sao Paulo', slug='sao-paulo', country=country)

        city = City.objects.create(
            region=region,
            country=country,
            name='Guarulhos',
            name_ascii='Guarulhos',
            slug='guarulhos')

        response = self.client.get('/scientific_mission/city_autocomplete/?q=Guarulhos')
        self.assertJSONEqual(
            force_text(response.content),
            '{"results": [{"selected_text": "Guarulhos, São Paulo, Brazil", "id": "' +
            str(city.id) +
            '", "text": "Guarulhos, São Paulo, Brazil"}], "pagination": {"more": false}}')

    def test_city_auto_complete_not_passing_q_argument(self):
        country = Country.objects.create(name='Brazil', name_ascii='Brazil', slug='brazil')
        region = Region.objects.create(name='São Paulo', name_ascii='Sao Paulo', slug='sao-paulo', country=country)

        city1 = City.objects.first()

        city2 = City.objects.create(
            region=region,
            country=country,
            name='Guarulhos',
            name_ascii='Guarulhos',
            slug='guarulhos')

        response = self.client.get('/scientific_mission/city_autocomplete/?q=')
        self.assertJSONEqual(
            force_text(response.content),
            '{"results": [' +
            '{"id": "' +
            str(city1.id) +
            '", "selected_text": "' +
            city1.name + ', ' + (city1.region.name + ', ' if city1.region else "") + city1.country.name +
            '", "text": ", "},' +
            '{"selected_text": "Guarulhos, São Paulo, Brazil", "id": "' +
            str(city2.id) +
            '", "text": "Guarulhos, São Paulo, Brazil"}], "pagination": {"more": false}}')

    def test_city_auto_complete_when_not_logged_returns_none_cities(self):
        country = Country.objects.create(name='Brazil', name_ascii='Brazil', slug='brazil')
        region = Region.objects.create(name='São Paulo', name_ascii='Sao Paulo', slug='sao-paulo', country=country)

        city = City.objects.create(
            region=region,
            country=country,
            name='Guarulhos',
            name_ascii='Guarulhos',
            slug='guarulhos')

        self.client.logout()

        response = self.client.get('/scientific_mission/city_autocomplete/?q=Guarulhos')
        self.assertJSONEqual(
            force_text(response.content),
            '{"results": [], "pagination": {"more": false}}')

        # Result if none wasn't being returned
        self.assertJSONNotEqual(
            force_text(response.content),
            '{"results": [{"selected_text": "Guarulhos, São Paulo, Brazil", "id": "' +
            str(city.id) +
            '", "text": "Guarulhos, São Paulo, Brazil"}], "pagination": {"more": false}}')

    def test_anexo_5_non_post_request_renders_anexo5_html_template(self):
        people = Person.objects.all()
        missions = ScientificMission.objects.all()
        date = datetime.datetime.now()

        response = self.client.get(reverse('anexo5'), {'people': people, 'missions': missions, 'default_date': date})
        self.assertTemplateUsed(response, 'anexo/anexo5.html')

    def test_anexo_5_rendered_template_have_success_in_presenting_data_passed(self):
        people = Person.objects.all()
        missions = ScientificMission.objects.all()
        date = datetime.datetime.now()

        response = self.client.get(reverse('anexo5'), {'people': people, 'missions': missions, 'default_date': date})
        self.assertContains(response, "<option value=" + str(people.first().id) + ">")

    def test_anexo_5_returns_message_when_process_number_is_all_zeros(self):
        people = Person.objects.all()
        missions = ScientificMission.objects.all()
        date = datetime.datetime.now()

        response = self.client.get(reverse('anexo5'), {'people': people, 'missions': missions, 'default_date': date})
        for message in response.context['messages']:
            self.assertEqual(
                message.message,
                mark_safe(_('You should have configured your process number on configurations. '
                            ' Click <a href="../../configuration">here</a> to configure it.')))

    def test_anexo_5_doesnt_returns_message_when_process_number_exists_and_it_is_not_is_all_zeros(self):
        ProcessNumber.objects.create(process_number='1111/11111-1')
        people = Person.objects.all()
        missions = ScientificMission.objects.all()
        date = datetime.datetime.now()

        response = self.client.get(reverse('anexo5'), {'people': people, 'missions': missions, 'default_date': date})
        self.assertTemplateUsed(response, 'anexo/anexo5.html')

    def test_anexo_5_post_request_without_principal_investigator_renders_todays_date_on_the_template(self):
        mission = ScientificMission.objects.first()
        title = mission.id
        date = datetime.datetime.now()
        issue_date = '06/10/2016'

        response = self.client.post(reverse('anexo5'), {'issue_date': issue_date,
                                                        'process': 000,
                                                        'title': title})
        self.assertContains(response, date.strftime("%d/%m/%Y"))
        self.assertNotContains(response, issue_date)

    def test_anexo_5_post_request_without_passing_issue_date_renders_todays_date_on_the_template(self):
        mission = ScientificMission.objects.first()
        title = mission.id
        date = datetime.datetime.now()

        response = self.client.post(reverse('anexo5'), {'issue_date': '',
                                                        'process': 000,
                                                        'title': title})
        self.assertContains(response, date.strftime("%d/%m/%Y"))

    def test_anexo_5_post_request_without_process_number_in_db_renders_pdf(self):
        person = Person.objects.first()
        PrincipalInvestigator.objects.create(name=person)
        mission = ScientificMission.objects.first()
        title = mission.id
        date = datetime.datetime.now()

        response = self.client.post(reverse('anexo5'), {'issue_date': date.strftime("%d/%m/%Y"),
                                                        'process': '',
                                                        'title': title})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('b\'%PDF' in str(response.content))

    def test_anexo_5_post_request_with_process_number_in_db_renders_pdf(self):
        ProcessNumber.objects.create(process_number='1111/11111-1')

        person = Person.objects.first()
        PrincipalInvestigator.objects.create(name=person)
        mission = ScientificMission.objects.first()
        title = mission.id
        date = datetime.datetime.now()

        response = self.client.post(reverse('anexo5'), {'issue_date': date.strftime("%d/%m/%Y"),
                                                        'process': '',
                                                        'title': title})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('b\'%PDF' in str(response.content))

    def test_anexo_5_post_request_without_mission_id_raises_error_message(self):
        date = datetime.datetime.now()

        response = self.client.post(reverse('anexo5'), {'issue_date': date.strftime("%d/%m/%Y"),
                                                        'process': 000,
                                                        'title': ''})
        for message in response.context['messages']:
            self.assertEqual(message.message, mark_safe(_('You have to choose a scientific mission!')))

    def test_anexo_5_post_request_with_inexisting_mission_id_raises_error_message(self):
        mission = ScientificMission.objects.first()
        title = mission.id+1
        date = datetime.datetime.now()

        response = self.client.post(reverse('anexo5'), {'issue_date': date.strftime("%d/%m/%Y"),
                                                        'process': 000,
                                                        'title': title})
        for message in response.context['messages']:
            self.assertEqual(message.message, mark_safe(_('No scientific mission matches the given query.')))

    def test_anexo_5_post_request_with_mission_without_routes_raises_message(self):
        person = Person.objects.first()
        mission = ScientificMission.objects.create(person=person, amount_paid=10)
        title = mission.id
        date = datetime.datetime.now()

        response = self.client.post(reverse('anexo5'), {'issue_date': date.strftime("%d/%m/%Y"),
                                                        'process': 000,
                                                        'title': title})
        for message in response.context['messages']:
            self.assertEqual(message.message, mark_safe(_("You should've set routes for this mission.")))

    def test_anexo_5_post_request_without_principal_investigator_raise_error_message(self):
        mission = ScientificMission.objects.first()
        title = mission.id
        date = datetime.datetime.now()

        response = self.client.post(reverse('anexo5'), {'issue_date': date.strftime("%d/%m/%Y"),
                                                        'process': 000,
                                                        'title': title})
        for message in response.context['messages']:
            self.assertEqual(message.message, mark_safe(_('You must set the Principal Investigator.')))

    def test_anexo_5_post_request_with_principal_investigator_renders_pdf(self):
        person = Person.objects.first()
        PrincipalInvestigator.objects.create(name=person)
        mission = ScientificMission.objects.first()
        title = mission.id
        date = datetime.datetime.now()

        response = self.client.post(reverse('anexo5'), {'issue_date': date.strftime("%d/%m/%Y"),
                                                        'process': 000,
                                                        'title': title})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('b\'%PDF' in str(response.content))

    def test_anexo_5_post_request_uses_anexo_5_pdf_html_template_with_valid_form(self):
        PrincipalInvestigator.objects.create(name=Person.objects.first())
        mission = ScientificMission.objects.first()
        title = mission.id
        date = datetime.datetime.now()

        response = self.client.post(reverse('anexo5'), {'issue_date': date.strftime("%d/%m/%Y"),
                                                        'process': 000,
                                                        'title': title})
        self.assertTemplateUsed(response, 'anexo/anexo5_pdf.html')

    def test_anexo_5_post_request_uses_anexo_5_html_template_with_invalid_form(self):
        PrincipalInvestigator.objects.create(name=Person.objects.first())
        response = self.client.post(reverse('anexo5'), {'issue_date': '',
                                                        'process': '',
                                                        'title': ''})

        self.assertTemplateUsed(response, 'anexo/anexo5.html')

    def test_anexo_6_get_request(self):
        response = self.client.get(reverse('anexo6'))
        self.assertEqual(response.status_code, 200)

    def test_anexo_6_post_request_with_process_number_in_db_renders_pdf(self):
        ProcessNumber.objects.create(process_number='1111/11111-1')
        PrincipalInvestigator.objects.create(name=Person.objects.first())

        response = self.client.post(reverse('anexo6'), {'value': 10,
                                                        'start_date': datetime.date(2019, 1, 1),
                                                        'end_date': datetime.date(2019, 1, 2),
                                                        'process': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('b\'%PDF' in str(response.content))

    def test_anexo_6_post_request_without_principal_investigator_raises_error_message(self):
        response = self.client.post(reverse('anexo6'))
        for message in response.context['messages']:
            self.assertEqual(message.message, mark_safe(_('You must set the Principal Investigator.')))

    def test_anexo_6_post_request_with_invalid_form_raises_error_message(self):
        PrincipalInvestigator.objects.create(name=Person.objects.first())
        response = self.client.post(reverse('anexo6'))
        for message in response.context['messages']:
            self.assertEqual(message.message, mark_safe(_('Your form is not valid.')))

    def test_anexo_6_post_request_with_valid_form_and_with_process_number_renders_pdf(self):
        PrincipalInvestigator.objects.create(name=Person.objects.first())

        response = self.client.post(reverse('anexo6'), {'value': 10,
                                                        'start_date': datetime.date(2019, 1, 1),
                                                        'end_date': datetime.date(2019, 1, 2),
                                                        'process': '0000/00000-0'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('b\'%PDF' in str(response.content))

    # Na prática, existe um impedimento em gerar o pdf quando não se digita o número do processo na view
    def test_anexo_6_post_request_with_valid_form_and_without_process_number_renders_pdf(self):
        PrincipalInvestigator.objects.create(name=Person.objects.first())

        response = self.client.post(reverse('anexo6'), {'value': 10,
                                                        'start_date': datetime.date(2019, 1, 1),
                                                        'end_date': datetime.date(2019, 1, 2),
                                                        'process': ''})

        self.assertEqual(response.status_code, 200)
        self.assertTrue('b\'%PDF' in str(response.content))

    def test_anexo_6_post_request_uses_anexo_6_pdf_html_template_with_valid_form(self):
        PrincipalInvestigator.objects.create(name=Person.objects.first())

        response = self.client.post(reverse('anexo6'), {'value': 10,
                                                        'start_date': datetime.date(2019, 1, 1),
                                                        'end_date': datetime.date(2019, 1, 2),
                                                        'process': '0000/00000-0'})
        self.assertTemplateUsed(response, 'anexo/anexo6_pdf.html')

    def test_anexo_6_post_request_uses_anexo_6_html_template_with_invalid_form(self):
        PrincipalInvestigator.objects.create(name=Person.objects.first())

        response = self.client.post(reverse('anexo6'))

        self.assertTemplateUsed(response, 'anexo/anexo6.html')

    def test_anexo_7_get_request(self):
        response = self.client.get(reverse('anexo7'))
        self.assertEqual(response.status_code, 200)

    def test_anexo_7_post_request_with_process_number_in_db_renders_pdf(self):
        ProcessNumber.objects.create(process_number='1111/11111-1')
        PrincipalInvestigator.objects.create(name=Person.objects.first())

        response = self.client.post(reverse('anexo7'), {'process': '',
                                                        'choice': 1,
                                                        'stretch': 'Test',
                                                        'person': Person.objects.first().id,
                                                        'value': 10,
                                                        'reimbursement': 0})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('b\'%PDF' in str(response.content))

    def test_anexo_7_post_request_with_invalid_form_raises_error_message(self):
        response = self.client.post(reverse('anexo7'))
        for message in response.context['messages']:
            self.assertEqual(message.message, mark_safe(_('Your form is not valid.')))

    def test_anexo_7_post_request_with_valid_form_and_principal_investigator_renders_pdf(self):
        PrincipalInvestigator.objects.create(name=Person.objects.first())
        response = self.client.post(reverse('anexo7'), {'process': 123,
                                                        'choice': 1,
                                                        'stretch': 'Test',
                                                        'person': Person.objects.first().id,
                                                        'value': 10,
                                                        'reimbursement': 0})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('b\'%PDF' in str(response.content))

    def test_anexo_7_post_request_without_principal_investigator_raises_error_messages(self):
        response = self.client.post(reverse('anexo7'), {'process': 123,
                                                        'choice': 1,
                                                        'stretch': 'Test',
                                                        'person': Person.objects.first().id,
                                                        'value': 10,
                                                        'reimbursement': 0})
        for message in response.context['messages']:
            self.assertEqual(message.message, mark_safe(_('You must set the Principal Investigator.')))

    # Na prática, existe um impedimento em gerar o pdf quando não se digita o número do processo na view
    def test_anexo_7_post_request_with_valid_form_and_without_process_number_renders_pdf(self):
        PrincipalInvestigator.objects.create(name=Person.objects.first())

        response = self.client.post(reverse('anexo7'), {'process': '',
                                                        'choice': 1,
                                                        'stretch': 'Test',
                                                        'person': Person.objects.first().id,
                                                        'value': 10,
                                                        'reimbursement': 0})

        self.assertEqual(response.status_code, 200)
        self.assertTrue('b\'%PDF' in str(response.content))

    def test_anexo_7_post_request_uses_anexo_7_pdf_html_template_with_valid_form(self):
        PrincipalInvestigator.objects.create(name=Person.objects.first())

        response = self.client.post(reverse('anexo7'), {'process': '',
                                                        'choice': 1,
                                                        'stretch': 'Test',
                                                        'person': Person.objects.first().id,
                                                        'value': 10,
                                                        'reimbursement': 0})
        self.assertTemplateUsed(response, 'anexo/anexo7_pdf.html')

    def test_anexo_7_post_request_uses_anexo_7_html_template_with_invalid_form(self):
        PrincipalInvestigator.objects.create(name=Person.objects.first())

        response = self.client.post(reverse('anexo7'))

        self.assertTemplateUsed(response, 'anexo/anexo7.html')

    def test_anexo_9_get_request(self):
        response = self.client.get(reverse('anexo9'))
        self.assertEqual(response.status_code, 200)

    def test_anexo_9_post_request_with_process_number_in_db_renders_pdf(self):
        ProcessNumber.objects.create(process_number='1111/11111-1')
        PrincipalInvestigator.objects.create(name=Person.objects.first())

        response = self.client.post(reverse('anexo9'), {'process': '',
                                                        'job': 'Test',
                                                        'person': Person.objects.first().id,
                                                        'value': 10})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('b\'%PDF' in str(response.content))

    def test_anexo_9_post_request_with_invalid_form_raises_error_message(self):
        response = self.client.post(reverse('anexo9'))
        for message in response.context['messages']:
            self.assertEqual(message.message, mark_safe(_('Your form is not valid.')))

    def test_anexo_9_post_request_with_valid_form_and_principal_investigator_renders_pdf(self):
        PrincipalInvestigator.objects.create(name=Person.objects.first())
        response = self.client.post(reverse('anexo9'), {'process': 123,
                                                        'job': 'Test',
                                                        'person': Person.objects.first().id,
                                                        'value': 10})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('b\'%PDF' in str(response.content))

    def test_anexo_9_post_request_without_principal_investigator_raises_error_messages(self):
        response = self.client.post(reverse('anexo9'), {'process': 123,
                                                        'job': 'Test',
                                                        'person': Person.objects.first().id,
                                                        'value': 10})
        for message in response.context['messages']:
            self.assertEqual(message.message, mark_safe(_('You must set the Principal Investigator.')))

    # Na prática, existe um impedimento em gerar o pdf quando não se digita o número do processo na view
    def test_anexo_9_post_request_with_valid_form_and_without_process_number_renders_pdf(self):
        PrincipalInvestigator.objects.create(name=Person.objects.first())

        response = self.client.post(reverse('anexo9'), {'process': '',
                                                        'job': 'Test',
                                                        'person': Person.objects.first().id,
                                                        'value': 10})

        self.assertEqual(response.status_code, 200)
        self.assertTrue('b\'%PDF' in str(response.content))

    def test_anexo_9_post_request_uses_anexo_9_pdf_html_template_with_valid_form(self):
        PrincipalInvestigator.objects.create(name=Person.objects.first())

        response = self.client.post(reverse('anexo9'), {'process': '',
                                                        'job': 'Test',
                                                        'person': Person.objects.first().id,
                                                        'value': 10})
        self.assertTemplateUsed(response, 'anexo/anexo9_pdf.html')

    def test_anexo_9_post_request_uses_anexo_9_html_template_with_invalid_form(self):
        PrincipalInvestigator.objects.create(name=Person.objects.first())

        response = self.client.post(reverse('anexo9'))

        self.assertTemplateUsed(response, 'anexo/anexo9.html')

    def test_mission_show_titles(self):
        response = self.client.get(reverse('anexo_missions'), {'person': Person.objects.first().id})
        self.assertContains(response, Person.objects.first().full_name + " - R$ 666.00")

    def test_mission_show_titles_post_request(self):
        response = self.client.post(reverse('anexo_missions'), {'person': Person.objects.first().id})
        self.assertEqual(response.status_code, 405)

    def test_get_missions(self):
        person = Person.objects.first()
        mission = ScientificMission.objects.create(person=person, amount_paid=13)
        country = Country.objects.create(name='Brazil', name_ascii='Brazil', slug='brazil')
        city = City.objects.create(country=country, name='Guarulhos', name_ascii='Guarulhos', slug='guarulhos')

        date_departure1 = timezone.now()
        date_arrival1 = timezone.now() + timezone.timedelta(3)

        Route.objects.create(
            scientific_mission=mission,
            origin_city=city,
            destination_city=city,
            departure=(date_departure1 + timezone.timedelta(1)).date(),
            arrival=(date_arrival1 + timezone.timedelta(2)).date(),
            order=0
        )

        missions = get_missions(date_departure1.date(), date_arrival1.date())
        self.assertEqual(missions[0]['mission'], mission)

    def test_get_missions_without_routes(self):
        for route in Route.objects.all():
            route.delete()
        person = Person.objects.first()
        mission = ScientificMission.objects.create(person=person, amount_paid=13)
        country = Country.objects.create(name='Brazil', name_ascii='Brazil', slug='brazil')
        city = City.objects.create(country=country, name='Guarulhos', name_ascii='Guarulhos', slug='guarulhos')

        date_departure1 = timezone.now()
        date_arrival1 = timezone.now() + timezone.timedelta(3)

        missions = get_missions(date_departure1.date(), date_arrival1.date())
        self.assertEqual(len(missions), 0)

    def test_missions_report_with_get_request(self):
        response = self.client.get(reverse('missions_report'))
        self.assertEqual(response.status_code, 200)

    def test_missions_report_with_get_request_uses_scientific_missions_html_template(self):
        response = self.client.get(reverse('missions_report'))
        self.assertTemplateUsed(response, 'report/scientific_mission/scientific_missions.html')

    def test_missions_report_post_request_with_invalid_form_raises_error_message(self):
        response = self.client.post(reverse('missions_report'), {'start_date': '', 'end_date': ''})
        for message in response.context['messages']:
            self.assertEqual(message.message, mark_safe(_('You entered a wrong date format or the end '
                                                          'date is not greater than or equal to the start date.')))

    def test_missions_report_post_request_with_end_date_sooner_than_start_date_raises_error_message(self):
        date_departure1 = timezone.now() - timezone.timedelta(367)
        date_arrival1 = timezone.now() + timezone.timedelta(1)

        response = self.client.post(
            reverse('missions_report'),
            {'start_date': date_departure1.date(), 'end_date': date_arrival1.date()})
        for message in response.context['messages']:
            self.assertEqual(message.message, _('You entered a wrong date format or the end '
                                                'date is not greater than or equal to the start date.'))

    def test_missions_report_post_request_with_appropriate_dates_renders_scientific_missions_report_html(self):
        date_departure1 = timezone.now() - timezone.timedelta(367)
        date_arrival1 = timezone.now() + timezone.timedelta(1)

        response = self.client.post(
            reverse('missions_report'),
            {'start_date': date_departure1.date().strftime("%d/%m/%Y"),
             'end_date': date_arrival1.date().strftime("%d/%m/%Y")})

        self.assertTemplateUsed(response, 'report/scientific_mission/scientific_missions_report.html')

    def test_missions_file_text_uses_scientific_missions_tex_template_when_passing_tex_as_extension(self):
        date_departure1 = timezone.now() - timezone.timedelta(367)
        date_arrival1 = timezone.now() + timezone.timedelta(1)

        response = self.client.get(
            reverse('scientific_missions_file'),
            {'start_date': date_departure1.date().strftime("%Y-%m-%d"),
             'end_date': date_arrival1.date().strftime("%Y-%m-%d"),
             'extension': '.tex'})

        self.assertTemplateUsed(response, 'report/scientific_mission/tex/scientific_missions.tex')

    def test_missions_file_text_renders_pdf_when_not_passing_tex_as_extension(self):
        date_departure1 = timezone.now() - timezone.timedelta(367)
        date_arrival1 = timezone.now() + timezone.timedelta(1)

        response = self.client.get(
            reverse('scientific_missions_file'),
            {'start_date': date_departure1.date().strftime("%Y-%m-%d"),
             'end_date': date_arrival1.date().strftime("%Y-%m-%d"),
             'extension': '.doc'})

        self.assertTemplateUsed(response, 'report/scientific_mission/pdf/scientific_missions.html')
        self.assertTrue('b\'%PDF' in str(response.content))
