from django.test import TestCase, RequestFactory

from django.contrib.admin.sites import AdminSite

from django.utils import timezone

from custom_auth.models import User
from person.models import Person
from activity.admin import TrainingProgramAdmin
from activity.models import TrainingProgram


USERNAME = "Test_user"
PASSWORD = "Test_psswd"


class TrainingProgramAdminTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD)
        self.user.is_active = True
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()

        self.factory = RequestFactory()

        self.logged = self.client.login(username=USERNAME, password=PASSWORD)

        self.user1 = User.objects.create_user(username=USERNAME + '0', password=PASSWORD + '0')

    def test_training_program_admin_returns_nothing_if_it_is_not_superuser(self):
        speaker = Person.objects.create(full_name='Person_Test')

        training_program = TrainingProgram.objects.create(
            title='Training_program_title',
            type_of_activity='t',
            start_date=timezone.now(),
            duration='1h')
        training_program.speaker.add(speaker)
        training_program.save()

        self.user.is_superuser = False
        self.user.save()
        training_program_admin = TrainingProgramAdmin(TrainingProgram, AdminSite())

        qs = training_program_admin.get_queryset(self)
        self.assertEqual(list(qs), [])

    def test_training_program_admin_returns_the_training_program_itself_if_it_is_superuser(self):
        speaker = Person.objects.create(full_name='Person_Test')

        training_program = TrainingProgram.objects.create(
            title='Training_program_title',
            type_of_activity='t',
            start_date=timezone.now(),
            duration='1h')
        training_program.speaker.add(speaker)
        training_program.save()

        training_program_admin = TrainingProgramAdmin(TrainingProgram, AdminSite())

        qs = training_program_admin.get_queryset(self)
        self.assertEqual(list(qs), [training_program])

    def test_training_program_admin_returns_the_training_program_itself_if_it_is_nira_admin(self):
        speaker = Person.objects.create(full_name='Person_Test')

        training_program = TrainingProgram.objects.create(
            title='Training_program_title',
            type_of_activity='t',
            start_date=timezone.now(),
            duration='1h')
        training_program.speaker.add(speaker)
        training_program.save()

        self.user.is_superuser = False
        self.user.is_nira_admin = True
        self.user.save()

        training_program_admin = TrainingProgramAdmin(TrainingProgram, AdminSite())

        qs = training_program_admin.get_queryset(self)
        self.assertEqual(list(qs), [training_program])
