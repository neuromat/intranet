from django.test import TestCase
from django.utils import timezone
from django.db.models import ProtectedError

from dissemination.models import ExternalMediaOutlet, InternalMediaOutlet, Topic, Dissemination, Internal, External


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


class DisseminationIntegrationModelTests(TestCase):
    def test_do_not_delete_internal_media_outlet_instance_if_there_is_internal_associated(self):
        self.assertEqual(InternalMediaOutlet.objects.count(), 0)
        self.assertEqual(Topic.objects.count(), 0)
        self.assertEqual(Internal.objects.count(), 0)

        internal_media_outlet = InternalMediaOutlet.objects.create(name='Internal_Media_Outlet_Test')

        topic = Topic.objects.create(name='Topic_Test')

        internal = Internal.objects.create(
            title='Title_Test',
            date=timezone.now(),
            link='http://test.com',
            type_of_media='i',
            media_outlet=internal_media_outlet)

        internal.topic.add(topic)
        internal.save()

        with self.assertRaises(ProtectedError) as e:
            internal_media_outlet.delete()

        self.assertEqual(InternalMediaOutlet.objects.last(), internal_media_outlet)
        self.assertEqual(Topic.objects.last(), topic)
        self.assertEqual(Internal.objects.last(), internal)

    def test_do_not_delete_external_media_outlet_instance_if_there_is_external_associated(self):
        self.assertEqual(ExternalMediaOutlet.objects.count(), 0)
        self.assertEqual(Topic.objects.count(), 0)
        self.assertEqual(External.objects.count(), 0)

        external_media_outlet = ExternalMediaOutlet.objects.create(name='External_Media_Outlet_Test')

        topic = Topic.objects.create(name='Topic_Test')

        external = External.objects.create(
            title='Title_Test',
            date=timezone.now(),
            link='http://test.com',
            type_of_media='i',
            media_outlet=external_media_outlet)

        external.topic.add(topic)
        external.save()

        with self.assertRaises(ProtectedError) as e:
            external_media_outlet.delete()

        self.assertEqual(ExternalMediaOutlet.objects.last(), external_media_outlet)
        self.assertEqual(Topic.objects.last(), topic)
        self.assertEqual(External.objects.last(), external)