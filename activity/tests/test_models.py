from django.test import TestCase

from activity.models import ProjectActivities, SeminarType
from person.models import Institution, InstitutionType


class ActivityModelTest(TestCase):

    def test_project_activity_string_representation_with_training_program(self):
        title = 'Dissimination activity'
        institution_type = InstitutionType.objects.create(name='Centro de Pesquisa')
        local = Institution.objects.create(name='FAPESP', type=institution_type)

        project_activity = ProjectActivities.objects.create(title=title, local=local, type_of_activity='t')

        self.assertEqual(project_activity.__str__(), 'Training Program - ' + title)

    def test_project_activity_string_representation_with_meeting(self):
        title = 'Dissimination activity'
        institution_type = InstitutionType.objects.create(name='Centro de Pesquisa')
        local = Institution.objects.create(name='FAPESP', type=institution_type)

        project_activity = ProjectActivities.objects.create(title=title, local=local, type_of_activity='m')

        self.assertEqual(project_activity.__str__(), 'Meeting - ' + title)

    def test_project_activity_string_representation_with_seminar(self):
        title = 'Dissimination activity'
        institution_type = InstitutionType.objects.create(name='Centro de Pesquisa')
        local = Institution.objects.create(name='FAPESP', type=institution_type)

        project_activity = ProjectActivities.objects.create(title=title, local=local, type_of_activity='s')

        self.assertEqual(project_activity.__str__(), 'Seminar - ' + title)

    def test_seminar_type_string_representation(self):
        name = 'Neuromat'
        seminar_type = SeminarType.objects.create(name=name)

        self.assertEqual(seminar_type.__str__(), name)
