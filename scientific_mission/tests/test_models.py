from django.test import TestCase

from person.models import Person, Institution
from scientific_mission.models import ScientificMission, Type

class ScientificMissionModelTest(TestCase):

    def test_type_string_representation(self):
        mission = 'Convenção anual'
        type = Type.objects.model(mission=mission)
        self.assertEqual(type.__str__(), mission)
