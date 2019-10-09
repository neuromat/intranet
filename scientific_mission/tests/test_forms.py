from django.test import TestCase

from scientific_mission.forms import ProcessField, AnnexSevenForm
from configuration.models import Person


class ProcessFieldFormTest(TestCase):
    def test_processfield_to_python(self):
        process_field = ProcessField()
        value = 1
        self.assertEqual(process_field.to_python(value), value)

    def test_processfield_validate(self):
        process_field = ProcessField()
        value = 1
        self.assertIsNone(process_field.validate(value))

    def test_processfield_clean(self):
        process_field = ProcessField()
        value = 1
        self.assertEqual(process_field.clean(value), value)


class AnnexSevenFormTest(TestCase):
    def setUp(self):
        self.person = Person.objects.create(full_name="Test_person")
        self.data = {'process': 123,
                     'choice': 1,
                     'stretch': 'Test',
                     'person': self.person.id,
                     'value': 10,
                     'reimbursement': 0}

    def test_name_is_principal_investigator_if_exists(self):
        annex_7_form = AnnexSevenForm(self.data)
        self.assertTrue(annex_7_form.is_valid())
