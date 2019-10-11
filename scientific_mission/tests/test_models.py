import datetime
from django.test import TestCase

from cities_light.models import City, Country

from scientific_mission.models import Type, ScientificMission, Route
from person.models import Person


class TypeTest(TestCase):

    def test_type_string_representation(self):
        mission = 'Convenção anual'
        mission_type = Type.objects.model(mission=mission)
        self.assertEqual(mission_type.__str__(), mission)


class ScientificMissionTest(TestCase):
    def setUp(self):
        self.person = Person.objects.create(full_name="Scientific Mission")
        self.amount_paid = '7'

    def test_scientific_mission_string_representation(self):
        scientific_mission = ScientificMission.objects.create(person=self.person, amount_paid=self.amount_paid)
        self.assertEqual(scientific_mission.__str__(), self.person.full_name + " - R$ " + self.amount_paid)

    def test_scientific_mission_value(self):
        scientific_mission = ScientificMission.objects.create(person=self.person, amount_paid=self.amount_paid)
        self.assertEqual(scientific_mission.value(), "R$ " + self.amount_paid)


class RouteTest(TestCase):
    def setUp(self):
        self.person = Person.objects.create(full_name="Scientific Mission")
        self.amount_paid = '7'
        self.scientific_mission = ScientificMission.objects.create(person=self.person, amount_paid=self.amount_paid)

        self.country = Country.objects.create(name="Country")
        self.city = City.objects.create(country=self.country)

    def test_route_save_with_db_empty(self):
        route = Route(scientific_mission=self.scientific_mission,
                      origin_city=self.city,
                      destination_city=self.city,
                      departure=datetime.date.today(),
                      arrival=datetime.date.today() - datetime.timedelta(1),
                      order=2)
        route.save()

        self.assertEqual(route.order, 1)

    def test_route_save_with_at_least_one_object_in_db(self):
        Route.objects.create(scientific_mission=self.scientific_mission,
                             origin_city=self.city,
                             destination_city=self.city,
                             departure=datetime.date.today(),
                             arrival=datetime.date.today() + datetime.timedelta(1),
                             order=1)

        route2 = Route(scientific_mission=self.scientific_mission,
                       origin_city=self.city,
                       destination_city=self.city,
                       departure=datetime.date.today() + datetime.timedelta(1),
                       arrival=datetime.date.today() + datetime.timedelta(2),
                       order=3)
        route2.save()

        self.assertEqual(route2.order, 2)

    def test_route_update_order(self):
        route = Route.objects.create(scientific_mission=self.scientific_mission,
                                     origin_city=self.city,
                                     destination_city=self.city,
                                     departure=datetime.date.today(),
                                     arrival=datetime.date.today() + datetime.timedelta(1),
                                     order=1)

        self.assertEqual(route.order, 1)

        route.order = 3
        route.save()

        self.assertEqual(route.order, 3)
