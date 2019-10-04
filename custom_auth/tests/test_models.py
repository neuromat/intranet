from django.test import TestCase

from custom_auth.models import UserManager, User


class CustomAuthTest(TestCase):
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
