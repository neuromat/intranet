from django.test import TestCase

from custom_auth.models import UserManager, User
from person.models import Person


class CustomAuthTest(TestCase):
    # pylint: disable=E1120, E1123
    def test_user_manager_creation_with_wrong_fields_raises_error(self):
        with self.assertRaises(TypeError):
            UserManager.create_user(nameuser='')

    def test_user_manager_creation_with_username_field_creates_innactive_user_instance(self):
        manager = User.objects.create_user(username='Test')
        self.assertIsInstance(manager, User)
        self.assertFalse(manager.is_active)

    def test_user_manager_creation_with_empty_username_field_raises_value_error(self):
        with self.assertRaisesMessage(ValueError, 'The username must be set'):
            User.objects.create_user(username='')

    # pylint: disable=E1120, E1123
    def test_superuser_manager_creation_with_wrong_fields_raises_error(self):
        with self.assertRaises(TypeError):
            UserManager.create_superuser(nameuser='')

    def test_superuser_manager_creation_with_username_and_password_fields_creates_active_superuser_instance(self):
        manager = User.objects.create_superuser(username='Test', password='Test')
        self.assertIsInstance(manager, User)
        self.assertTrue(manager.is_active)
        self.assertTrue(manager.is_superuser)

    def test_superuser_manager_creation_with_empty_username_field_raises_value_error(self):
        with self.assertRaisesMessage(ValueError, 'The username must be set'):
            User.objects.create_superuser(username='', password='')

    def test_user_str_representation(self):
        username = 'Test'
        manager = User.objects.create_user(username=username)
        self.assertEqual(manager.__str__(), username)

    def test_user_shortname_representation(self):
        username = 'Test'
        manager = User.objects.create_user(username=username)
        self.assertEqual(manager.get_short_name(), username)


class CustomAuthIntegrationTest(TestCase):
    def test_delete_person_instance_that_have_a_user_deletes_the_user_too(self):
        self.assertEqual(Person.objects.count(), 0)
        self.assertEqual(User.objects.count(), 0)

        person = Person.objects.create(full_name='Speaker_Test')
        user = User.objects.create(user_profile=person)

        self.assertEqual(Person.objects.last(), person)
        self.assertEqual(User.objects.last(), user)

        person.delete()

        self.assertEqual(Person.objects.count(), 0)
        self.assertEqual(User.objects.count(), 0)
