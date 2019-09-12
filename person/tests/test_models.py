from django.test import TestCase

from person.models import Person, Institution, Role, InstitutionType


class PersonModelTest(TestCase):

    def test_person_string_reprentation(self):
        full_name = 'Nildo'
        person = Person.objects.create(full_name=full_name)

        self.assertEqual(person.__str__(), full_name)


    def test_institution_string_reprentation(self):
        name = 'FAPESP'
        institution = Institution(name=name)

        self.assertEqual(institution.__str__(), name)

    def test_role_string_representation(self):
        name = 'Associate Investigator'
        role = Role.objects.create(name='Associate Investigator')

        self.assertEqual(role.__str__(), name)

    def test_institution_type_string_representation(self):
        name = 'Fundação'
        institution_type = InstitutionType.objects.create(name='Fundação')

        self.assertEqual(institution_type.__str__(), name)