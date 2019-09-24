from django.test import TestCase

from scientific_mission.models import Type


class ScientificMissionModelTest(TestCase):

    def test_type_string_representation(self):
        mission = 'Convenção anual'
        mission_type = Type.objects.model(mission=mission)
        self.assertEqual(mission_type.__str__(), mission)
