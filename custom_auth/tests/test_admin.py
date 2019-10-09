from django.test import TestCase, RequestFactory

from django.contrib.admin.sites import AdminSite

from custom_auth.admin import CustomUserAdmin
from custom_auth.models import User

USERNAME = "Test_user"
PASSWORD = "Test_psswd"


def system_authentication(instance):
    user = User.objects.create_user(username=USERNAME, password=PASSWORD)
    user.is_active = True
    user.is_staff = True
    user.is_superuser = True
    user.save()
    factory = RequestFactory()
    logged = instance.client.login(username=USERNAME, password=PASSWORD)
    return logged, user, factory


class CustomUserAdminTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username=USERNAME + '0', password=PASSWORD + '0')

    def test_custom_user_admin_returns_the_user_itself_if_it_is_not_superuser(self):
        logged, self.user, self.factory = system_authentication(self)
        self.user.is_superuser = False
        self.user.save()
        custom_user_admin = CustomUserAdmin(User, AdminSite())

        qs = custom_user_admin.get_queryset(self)
        self.assertEqual(list(qs), [self.user])

    def test_custom_user_admin_returns_all_users_if_it_is_not_superuser(self):
        logged, self.user, self.factory = system_authentication(self)
        custom_user_admin = CustomUserAdmin(User, AdminSite())

        qs = custom_user_admin.get_queryset(self)
        self.assertEqual(list(qs), [self.user1, self.user])

    def test_get_fieldsets_when_superuser(self):
        logged, self.user, self.factory = system_authentication(self)
        custom_user_admin = CustomUserAdmin(User, AdminSite())
        fields = custom_user_admin.get_fieldsets(self)

        fields_expected = [(None, {'fields': ('username', 'password1', 'password2')})]
        self.assertEqual(list(fields), fields_expected)

    def test_get_fieldsets_when_not_superuser(self):
        logged, self.user, self.factory = system_authentication(self)
        self.user.is_superuser = False
        self.user.save()
        custom_user_admin = CustomUserAdmin(User, AdminSite())
        fields = custom_user_admin.get_fieldsets(self)

        fields_expected = [(None, {'fields': ('username', 'password')})]
        self.assertEqual(list(fields), fields_expected)
