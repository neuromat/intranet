from django.test import TestCase
from django.utils import timezone

from dissemination.models import ExternalMediaOutlet, InternalMediaOutlet, Topic, Dissemination


class DisseminationModelTests(TestCase):

    def test_topic_string_representation(self):
        name = 'Neuromat experiments'
        topic = Topic.objects.create(name=name)

        self.assertEqual(topic.__str__(), name)

    def test_internal_media_outlet_string_representation(self):
        name = 'Newsletter'
        internal_media_outlet = InternalMediaOutlet.objects.create(name=name)

        self.assertEqual(internal_media_outlet.__str__(), name)

    def test_external_media_outlet_string_representation(self):
        name = 'Agência FAPESP'
        external_media_outlet = ExternalMediaOutlet.objects.create(name=name)

        self.assertEqual(external_media_outlet.__str__(), name)

    def test_dissemination_string_representation(self):
        title = 'Title Test'
        date = timezone.now()
        dissemination = Dissemination.objects.create(title=title, date=date)

        self.assertEqual(dissemination.__str__(), title)
