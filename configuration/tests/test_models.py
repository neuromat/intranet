from django.test import TestCase

from person.models import Person
from configuration.models import PrincipalInvestigator


class ConfigurationIntegrationTest(TestCase):
    def test_delete_person_instance_that_it_is_also_principal_investigator_deletes_the_principal_investigator(self):
        self.assertEqual(Person.objects.count(), 0)
        self.assertEqual(PrincipalInvestigator.objects.count(), 0)

        person = Person.objects.create(full_name='Speaker_Test')
        principal_investigator = PrincipalInvestigator.objects.create(name=person)

        self.assertEqual(Person.objects.last(), person)
        self.assertEqual(PrincipalInvestigator.objects.last(), principal_investigator)

        person.delete()

        self.assertEqual(Person.objects.count(), 0)
        self.assertEqual(PrincipalInvestigator.objects.count(), 0)
