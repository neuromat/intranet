import datetime
from django.urls import reverse
from django.test import TestCase
from cities_light.models import City, Country
from scientific_mission.models import ScientificMission, Route
from person.models import Person, Role
from research.tests.test_orig import system_authentication
from django.utils import timezone


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

    def test_anexo(self):

        people = Person.objects.all()
        missions = ScientificMission.objects.all()
        date = datetime.datetime.now()

        # If Not a POST request:
        response = self.client.get(reverse('anexo5'), {'people': people,
                                                       'missions': missions,
                                                       'default_date': date})
        self.assertEqual(response.status_code, 200)

        # Else: its a POST then we go to the other tests...

        # Valid id
        mission = missions[0]
        title = mission.pk

        # Date typed
        response = self.client.post(reverse('anexo5'), {'issue_date': '06/10/2016',
                                                        'process': 000,
                                                        'title': title})
        self.assertEqual(response.status_code, 200)

        # Without date
        response = self.client.post(reverse('anexo5'), {'issue_date': '',
                                                        'process': 000,
                                                        'title': title})
        self.assertEqual(response.status_code, 200)

        # Test if mission id exists
        response = self.client.post(reverse('anexo5'), {'issue_date': '08/03/2015',
                                                        'process': 000,
                                                        'title': ''})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('anexo5'), {'issue_date': '07/05/2014',
                                                        'process': 000,
                                                        'title': title})
        self.assertEqual(response.status_code, 200)

        # Invalid id: 404
        response = self.client.post(reverse('anexo5'), {'issue_date': '25/12/1997',
                                                        'process': 000,
                                                        'title': -3})
        self.assertEqual(response.status_code, 404)

        # Show titles
        person = people[0]
        person_id = person.pk
        response = self.client.get(reverse('anexo_missions'), {'person': person_id})
        self.assertEqual(response.status_code, 200)
