from django.test import TestCase
from django.db.models import ProtectedError
from django.utils import timezone

from cities_light.models import City, Country

from scientific_mission.models import Type, ScientificMission, Route, ProjectActivities
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
                      departure=timezone.now(),
                      arrival=timezone.now() - timezone.timedelta(1),
                      order=2)
        route.save()

        self.assertEqual(route.order, 1)

    def test_route_save_with_at_least_one_object_in_db(self):
        Route.objects.create(scientific_mission=self.scientific_mission,
                             origin_city=self.city,
                             destination_city=self.city,
                             departure=timezone.now(),
                             arrival=timezone.now() + timezone.timedelta(1),
                             order=1)

        route2 = Route(scientific_mission=self.scientific_mission,
                       origin_city=self.city,
                       destination_city=self.city,
                       departure=timezone.now() + timezone.timedelta(1),
                       arrival=timezone.now() + timezone.timedelta(2),
                       order=3)
        route2.save()

        self.assertEqual(route2.order, 2)

    def test_route_update_order(self):
        route = Route.objects.create(scientific_mission=self.scientific_mission,
                                     origin_city=self.city,
                                     destination_city=self.city,
                                     departure=timezone.now(),
                                     arrival=timezone.now() + timezone.timedelta(1),
                                     order=1)

        self.assertEqual(route.order, 1)

        route.order = 3
        route.save()

        self.assertEqual(route.order, 3)


class ScientificMissionAppIntegrationTest(TestCase):
    def test_do_not_delete_person_instance_if_there_is_scientific_mission_associated(self):
        self.assertEqual(Person.objects.count(), 0)
        self.assertEqual(ScientificMission.objects.count(), 0)

        person = Person.objects.create(full_name='Person_Test')

        scientific_mission = ScientificMission.objects.create(person=person, amount_paid=10)

        with self.assertRaises(ProtectedError) as e:
            person.delete()

        self.assertEqual(Person.objects.last(), person)
        self.assertEqual(ScientificMission.objects.last(), scientific_mission)

    def test_do_not_delete_project_activities_instance_if_there_is_scientific_mission_associated(self):
        self.assertEqual(Person.objects.count(), 0)
        self.assertEqual(ProjectActivities.objects.count(), 0)
        self.assertEqual(ScientificMission.objects.count(), 0)

        person = Person.objects.create(full_name='Person_Test')

        project_activities = ProjectActivities.objects.create(
            title='Porject_Activities_Test',
            type_of_activity='s')

        scientific_mission = ScientificMission.objects.create(
            person=person,
            amount_paid=10,
            project_activity=project_activities)

        with self.assertRaises(ProtectedError) as e:
            project_activities.delete()

        self.assertEqual(Person.objects.last(), person)
        self.assertEqual(ProjectActivities.objects.last(), project_activities)
        self.assertEqual(ScientificMission.objects.last(), scientific_mission)

    def test_do_not_delete_city_instance_if_there_is_scientific_mission_associated(self):
        self.assertEqual(Person.objects.count(), 0)
        self.assertEqual(Country.objects.count(), 0)
        self.assertEqual(City.objects.count(), 0)
        self.assertEqual(ScientificMission.objects.count(), 0)

        person = Person.objects.create(full_name='Person_Test')

        country = Country.objects.create(name="Country")
        city = City.objects.create(country=country)

        scientific_mission = ScientificMission.objects.create(
            person=person,
            amount_paid=10,
            destination_city=city)

        with self.assertRaises(ProtectedError) as e:
            city.delete()

        self.assertEqual(Person.objects.last(), person)
        self.assertEqual(Country.objects.last(), country)
        self.assertEqual(City.objects.last(), city)
        self.assertEqual(ScientificMission.objects.last(), scientific_mission)

    def test_do_not_delete_city_instance_if_there_is_route_origin_city_associated(self):
        self.assertEqual(Person.objects.count(), 0)
        self.assertEqual(Country.objects.count(), 0)
        self.assertEqual(City.objects.count(), 0)
        self.assertEqual(ScientificMission.objects.count(), 0)
        self.assertEqual(Route.objects.count(), 0)

        person = Person.objects.create(full_name='Person_Test')

        country = Country.objects.create(name='Country')
        city_1 = City.objects.create(name='City_1', country=country)
        city_2 = City.objects.create(name='City_2', country=country)

        scientific_mission = ScientificMission.objects.create(
            person=person,
            amount_paid=10)

        route = Route.objects.create(
            scientific_mission=scientific_mission,
            origin_city=city_1,
            destination_city=city_2,
            departure=timezone.now(),
            arrival=timezone.now(),
            order=1)

        with self.assertRaises(ProtectedError) as e:
            city_1.delete()

        self.assertEqual(Person.objects.last(), person)
        self.assertEqual(Country.objects.last(), country)
        self.assertEqual(City.objects.first(), city_1)
        self.assertEqual(ScientificMission.objects.last(), scientific_mission)
        self.assertEqual(Route.objects.last(), route)

    def test_do_not_delete_city_instance_if_there_is_route_destination_city_associated(self):
        self.assertEqual(Person.objects.count(), 0)
        self.assertEqual(Country.objects.count(), 0)
        self.assertEqual(City.objects.count(), 0)
        self.assertEqual(ScientificMission.objects.count(), 0)
        self.assertEqual(Route.objects.count(), 0)

        person = Person.objects.create(full_name='Person_Test')

        country = Country.objects.create(name='Country')
        city_1 = City.objects.create(name='City_1', country=country)
        city_2 = City.objects.create(name='City_2', country=country)

        scientific_mission = ScientificMission.objects.create(
            person=person,
            amount_paid=10)

        route = Route.objects.create(
            scientific_mission=scientific_mission,
            origin_city=city_1,
            destination_city=city_2,
            departure=timezone.now(),
            arrival=timezone.now(),
            order=1)

        with self.assertRaises(ProtectedError) as e:
            city_2.delete()

        self.assertEqual(Person.objects.last(), person)
        self.assertEqual(Country.objects.last(), country)
        self.assertEqual(City.objects.last(), city_2)
        self.assertEqual(ScientificMission.objects.last(), scientific_mission)
        self.assertEqual(Route.objects.last(), route)

    def test_delete_route_instance_associated_with_scientific_mission_when_this_one_is_deleted(self):
        self.assertEqual(Person.objects.count(), 0)
        self.assertEqual(Country.objects.count(), 0)
        self.assertEqual(City.objects.count(), 0)
        self.assertEqual(ScientificMission.objects.count(), 0)
        self.assertEqual(Route.objects.count(), 0)

        person = Person.objects.create(full_name='Person_Test')

        country = Country.objects.create(name='Country')
        city_1 = City.objects.create(name='City_1', country=country)
        city_2 = City.objects.create(name='City_2', country=country)

        scientific_mission = ScientificMission.objects.create(
            person=person,
            amount_paid=10)

        Route.objects.create(
            scientific_mission=scientific_mission,
            origin_city=city_1,
            destination_city=city_2,
            departure=timezone.now(),
            arrival=timezone.now(),
            order=1)

        scientific_mission.delete()

        self.assertEqual(Person.objects.count(), 1)
        self.assertEqual(Country.objects.count(), 1)
        self.assertEqual(City.objects.count(), 2)
        self.assertEqual(ScientificMission.objects.count(), 0)
        self.assertEqual(Route.objects.count(), 0)
