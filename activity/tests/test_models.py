from django.test import TestCase
from django.db.models import ProtectedError
from django.utils import timezone

from activity.models import ProjectActivities, SeminarType, News, Meeting, TrainingProgram, Seminar
from person.models import Institution, InstitutionType, Person


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


class ActivityIntegrationTest(TestCase):
    def test_do_not_delete_institution_instance_if_there_is_project_activity_associated(self):
        self.assertEqual(InstitutionType.objects.count(), 0)
        self.assertEqual(Institution.objects.count(), 0)
        self.assertEqual(ProjectActivities.objects.count(), 0)

        institution_type = InstitutionType.objects.create(name='InstitutionType_Test')
        institution = Institution.objects.create(name='Institution_Test', type=institution_type)

        project_activity = ProjectActivities.objects.create(title='Title', local=institution, type_of_activity='t')

        with self.assertRaises(ProtectedError) as e:
            institution.delete()

        self.assertEqual(InstitutionType.objects.last(), institution_type)
        self.assertEqual(Institution.objects.last(), institution)
        self.assertEqual(ProjectActivities.objects.last(), project_activity)

    def test_delete_news_instance_associated_with_project_activity_when_this_one_is_deleted(self):
        self.assertEqual(ProjectActivities.objects.count(), 0)
        self.assertEqual(News.objects.count(), 0)

        project_activity = ProjectActivities.objects.create(title='Title', type_of_activity='t')
        news = News.objects.create(activity=project_activity, url='https://test.com')

        self.assertEqual(ProjectActivities.objects.last(), project_activity)
        self.assertEqual(News.objects.last(), news)

        project_activity.delete()

        self.assertEqual(ProjectActivities.objects.count(), 0)
        self.assertEqual(News.objects.count(), 0)

    def test_do_not_delete_meeting_instance_if_there_is_training_program_associated(self):
        self.assertEqual(Person.objects.count(), 0)
        self.assertEqual(Meeting.objects.count(), 0)
        self.assertEqual(TrainingProgram.objects.count(), 0)

        speaker = Person.objects.create(full_name='Speaker_Test')

        meeting = Meeting.objects.create(
            title='Meeting_type',
            type_of_activity='t',
            start_date=timezone.now(),
            end_date=timezone.now())

        training_program = TrainingProgram.objects.create(
            title='Training_program_title',
            type_of_activity='t',
            belongs_to=meeting,
            start_date=timezone.now(),
            duration='1h')
        training_program.speaker.add(speaker)
        training_program.save()

        with self.assertRaises(ProtectedError) as e:
            meeting.delete()

        self.assertEqual(Person.objects.last(), speaker)
        self.assertEqual(Meeting.objects.last(), meeting)
        self.assertEqual(TrainingProgram.objects.last(), training_program)

    def test_do_not_delete_meeting_instance_if_there_is_seminar_associated(self):
        self.assertEqual(Person.objects.count(), 0)
        self.assertEqual(Meeting.objects.count(), 0)
        self.assertEqual(SeminarType.objects.count(), 0)
        self.assertEqual(Seminar.objects.count(), 0)

        speaker = Person.objects.create(full_name='Speaker_Test')

        meeting = Meeting.objects.create(
            title='Meeting_type',
            type_of_activity='t',
            start_date=timezone.now(),
            end_date=timezone.now())

        seminar_type = SeminarType.objects.create(name='Seminar_Type')
        seminar = Seminar.objects.create(
            title='Seminar_title',
            type_of_activity='s',
            belongs_to=meeting,
            category=seminar_type,
            date=timezone.now(),
        )

        seminar.speaker.add(speaker)
        seminar.save()

        with self.assertRaises(ProtectedError) as e:
            meeting.delete()

        self.assertEqual(Person.objects.last(), speaker)
        self.assertEqual(Meeting.objects.last(), meeting)
        self.assertEqual(SeminarType.objects.last(), seminar_type)
        self.assertEqual(Seminar.objects.last(), seminar)

    def test_do_not_delete_seminar_type_instance_if_there_is_seminar_associated(self):
        self.assertEqual(Person.objects.count(), 0)
        self.assertEqual(SeminarType.objects.count(), 0)
        self.assertEqual(Seminar.objects.count(), 0)

        speaker = Person.objects.create(full_name='Speaker_Test')

        seminar_type = SeminarType.objects.create(name='Seminar_Type')
        seminar = Seminar.objects.create(
            title='Seminar_title',
            type_of_activity='s',
            category=seminar_type,
            date=timezone.now(),
        )

        seminar.speaker.add(speaker)
        seminar.save()

        with self.assertRaises(ProtectedError) as e:
            seminar_type.delete()

        self.assertEqual(Person.objects.last(), speaker)
        self.assertEqual(SeminarType.objects.last(), seminar_type)
        self.assertEqual(Seminar.objects.last(), seminar)