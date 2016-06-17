import datetime
from django.core.urlresolvers import reverse
from django.test import TestCase
from cities_light.models import City, Country
from scientific_mission.models import ScientificMission
from person.models import Person
from research.tests import system_authentication


# Create a scientific mission for testing
def scientific_mission(person, city, departure, arrival, amount_paid):
    return ScientificMission(person=person,
                             origin_city=city, destination_city=city,
                             departure=departure, arrival=arrival, amount_paid=amount_paid)


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

        country = Country(id=31)
        country.save()

        city = City(country=country)
        city.save()

        person = Person(full_name="Fulano Testeiro")
        person.save()

        departure1 = datetime.date(2015, 1, 15)
        arrival1 = datetime.date(2015, 1, 16)

        departure2 = datetime.date(2014, 1, 15)
        arrival2 = datetime.date(2014, 1, 16)

        amount_paid = 666

        mission1 = scientific_mission(person, city, departure1, arrival1, amount_paid)
        mission1.save()

        mission2 = scientific_mission(person, city, departure2, arrival2, amount_paid)
        mission2.save()

    def test_report(self):

        # With nothing
        response = self.client.get(reverse('missions_report'))
        self.assertEqual(response.status_code, 200)

        # With date
        response = self.client.post(reverse('missions_report'), {'start_date': '01-01-2015',
                                                                 'end_date': '03-05-2017'})
        cont = response.context['missions']
        self.assertEqual(len(cont), 1)
        self.assertEqual(response.status_code, 200)

        # Without date
        response = self.client.post(reverse('missions_report'), {'start_date': '',
                                                                 'end_date': ''})
        cont = response.context['missions']
        self.assertEqual(len(cont), 2)
        self.assertEqual(response.status_code, 200)

        # Wrong dates
        response = self.client.post(reverse('missions_report'), {'start_date': '01-01-2016',
                                                                 'end_date': '03-05-2015'})
        self.assertEqual(response.status_code, 200)

    def test_tex(self):
        response = self.client.get(reverse('scientific_missions_tex'), {'start_date': '2015-03-01',
                                                                        'end_date': '2017-03-05'})
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
        id = mission.pk

        # Date typed
        response = self.client.post(reverse('anexo5'), {'issue_date': '06/10/2016',
                                                        'process': 000,
                                                        'title': id})
        self.assertEqual(response.status_code, 200)

        # Without date
        response = self.client.post(reverse('anexo5'), {'issue_date': '',
                                                        'process': 000,
                                                        'title': id})
        self.assertEqual(response.status_code, 200)

        # Test if mission id exists
        response = self.client.post(reverse('anexo5'), {'issue_date': '08/03/2015',
                                                        'process': 000,
                                                        'title': ''})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('anexo5'), {'issue_date': '07/05/2014',
                                                        'process': 000,
                                                        'title': id})
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
