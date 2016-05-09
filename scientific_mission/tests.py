import datetime
from django.core.urlresolvers import reverse
from django.test import TestCase
from cities_light.models import City, Country
from models import ScientificMission
from person.models import Person
from research.tests import system_authentication


# Create a scientific mission for testing, with origin and destination already set
def scientific_mission(person, departure, arrival, amount_paid):

    # Origin country: Brazil
    # Origin city: Alegrete, Rio Grande do Sul
    # o_country = Country.objects.filter(id=31)
    # o_city = City.objects.filter(id=2130)

    # Destination country: United States
    # Destination city is: Albany, California
    # d_country = Country.objects.filter(id=234)
    # d_city = City.objects.filter(id=21470)

    """
    return ScientificMission(person=person,
                             origin_country=o_country, origin_city=o_city,
                             destination_country=d_country, destination_city=d_city,
                             departure=departure, arrival=arrival, amount_paid=amount_paid)
    """

    country = Country()
    country.save()
    city = City(country=country)
    city.save()

    return ScientificMission(person=person,
                             origin_country=country, origin_city=city,
                             destination_country=country, destination_city=city,
                             departure=departure, arrival=arrival, amount_paid=amount_paid)


class ScientificMissionsTest(TestCase):

    def setUp(self):
        logged, self.user, self.factory = system_authentication(self)
        self.assertEqual(logged, True)

        person = Person(full_name="Fulano Testeiro")
        person.save()

        departure = datetime.date(2015, 1, 15)
        arrival = datetime.date(2015, 1, 16)

        amount_paid = 666

        mission_example = scientific_mission(person, departure, arrival, amount_paid)
        mission_example.save()

    def test_select_cities(self):
        pass

    def test_load_origin_cities(self):
        pass

    def test_missions_report_with_date(self):
        response = self.client.post(reverse('missions_report'), {'start_date': '01-01-2015',
                                                                 'end_date': '03-05-2017'})
        cont = response.context['missions']
        self.assertEqual(len(cont), 1)
        self.assertEqual(response.status_code, 200)

    def test_missions_report_without_date(self):

        response = self.client.post(reverse('missions_report'), {'start_date': '',
                                                                 'end_date': ''})
        cont = response.context['missions']
        self.assertEqual(len(cont), 1)
        self.assertEqual(response.status_code, 200)