from django.test import TestCase

from activity.models import ProjectActivities, SeminarType
from person.models import Institution


class ActivityModelTest(TestCase):

    # def test_project_activity_string_representation(self):
    #     title = 'Dissimination activity'
    #     local = Institution.objects.create(name='FAPESP')
    #
    #     # Defining types of activities
    #     TRAINING_PROGRAM = 't'
    #     MEETING = 'm'
    #     SEMINAR = 's'
    #     TYPE_OF_ACTIVITY = (
    #         (TRAINING_PROGRAM, _('Training Program')),
    #         (MEETING, _('Meeting')),
    #         (SEMINAR, _('Seminar')),
    #     )
    #
    #     project_activity = ProjectActivities.objects.create(title=title, local=local, type_of_activity=TYPE_OF_ACTIVITY)
    #
    #     self.assertEqual(project_activity.__str__(), title)


    def test_seminar_type_string_representation(self):
        name = 'Neuromat'
        seminar_type = SeminarType.objects.create(name=name)

        self.assertEqual(seminar_type.__str__(), name)
