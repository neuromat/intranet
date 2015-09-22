from custom_auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory
from models import AcademicWork, TypeAcademicWork, Person


USER_USERNAME = 'myadmin'
USER_PWD = 'mypassword'


class ResearchValidation(TestCase):

    user = ''
    academic_work = None
    advisee = None
    advisor = None

    postdoc_01 = None
    postdoc_02 = None

    def setUp(self):
        self.user = User.objects.create_user(username=USER_USERNAME, password=USER_PWD)
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()

        self.factory = RequestFactory()

        logged = self.client.login(username=USER_USERNAME, password=USER_PWD)
        self.assertEqual(logged, True)

        academic_work = TypeAcademicWork.objects.create(name='Post-doctoral')
        academic_work.save()

        advisee = Person.objects.create(full_name='John Smith')
        advisee.save()

        advisor = Person.objects.create(full_name='Emma Miller')
        advisor.save()

        # First academic work
        postdoc_01 = AcademicWork()
        postdoc_01.type = academic_work
        postdoc_01.advisee = advisee
        postdoc_01.advisor = advisor
        postdoc_01.start_date = '2013-08-20'
        postdoc_01.end_date = '2014-08-26'
        postdoc_01.save()

        # Second academic work
        postdoc_02 = AcademicWork()
        postdoc_02.type = academic_work
        postdoc_02.advisee = advisee
        postdoc_02.advisor = advisor
        postdoc_02.start_date = '2013-08-20'
        postdoc_02.end_date = '2014-08-26'
        postdoc_02.save()

    def test_current_report(self):
        start_date = '01-07-2014'
        end_date = '31-07-2015'

        response = self.client.post(reverse('academic_works'), {'start_date': start_date, 'end_date': end_date})

        self.assertEqual(len(response.context['postdoc_concluded']), 1)
