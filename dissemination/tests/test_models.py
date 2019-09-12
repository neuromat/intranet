from django.test import TestCase

from dissemination.models import ExternalMediaOutlet, InternalMediaOutlet, Topic


class DisseminationModelTests(TestCase):

    def test_topic_string_representation(self):
        name = 'Neuromat experiments'
        topic = Topic.objects.create(name='Neuromat experiments')

        self.assertEqual(topic.__str__(), name)

    def test_internal_media_outlet_string_representation(self):

        name = 'Newsletter'
        internal_media_outlet = InternalMediaOutlet.objects.create(name='Newsletter')

        self.assertEqual(internal_media_outlet.__str__(), name)

    def test_external_media_outlet_string_representation(self):

        name = 'Agência FAPESP'
        external_media_outlet = ExternalMediaOutlet.objects.create(name='Agência FAPESP')

        self.assertEqual(external_media_outlet.__str__(), name)
