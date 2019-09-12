from django.test import TestCase

from research.models import TypeAcademicWork


class ResearchModelTests(TestCase):

    def test_type_academic_work_string_representation(self):
        name = 'PhD'
        type_academic_work = TypeAcademicWork.objects.create(name='PhD')

        self.assertEqual(type_academic_work.__str__(), name)