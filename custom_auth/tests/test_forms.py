from django.test import TestCase

from custom_auth.forms import UserCreationForm, UserChangeForm
from custom_auth.models import User


class UserFormsTest(TestCase):
    def test_user_creation_form_is_valid(self):
        username = 'Test'
        password = 'psswrd'
        data = {'username': username, 'password1': password, 'password2': password}
        form = UserCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_user_creation_fails_when_a_duplicate_username_is_passed_and_raises_message(self):
        username = 'Test'
        password = 'psswrd'
        User.objects.create_superuser(username, 'test_manager_password')

        data = {'username': username, 'password1': password, 'password2': password}
        form = UserCreationForm(data=data)
        self.assertIn('username', form.errors.keys())
        self.assertIn('Duplicate username', form.errors['username'])

    def test_non_matching_passwords_raises_error_messages(self):
        password1 = 'psswrd1'
        password2 = 'psswrd2'
        data = {'username': 'Test', 'password1': password1, 'password2': password2}
        form = UserCreationForm(data=data)
        self.assertIn('password2', form.errors.keys())
        self.assertIn('Passwords do not match', form.errors['password2'])

    def test_user_creation_form_creates_a_hash_for_the_user_password(self):
        password = 'psswrd'
        data = {'username': 'Test', 'password1': password, 'password2': password}
        form = UserCreationForm(data=data)
        form.save()
        self.assertNotEqual(password, User.objects.first().password)

    def test_user_creation_form_creates_a_hash_for_the_user_password_but_dont_save_the_user_with_commit_set_false(self):
        password = 'psswrd'
        data = {'username': 'Test', 'password1': password, 'password2': password}
        form = UserCreationForm(data=data)
        form.save(commit=False)
        self.assertEqual(User.objects.count(), 0)

    def test_user_update_clean_password_returns_initial_hash_for_that_user(self):
        username = 'Test'
        password = 'psswrd'

        user = User.objects.create_user(username, password)

        new_password = 'nw_psswrd'
        data_update = {'username': username, 'password': new_password}
        form_update = UserChangeForm(data=data_update, instance=user)

        self.assertEqual(form_update.clean_password(), user.password)
