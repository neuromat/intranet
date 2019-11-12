from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError

from person.models import Person, Institution, Role, InstitutionType, CitationName, validate_cpf
from custom_auth.models import User
from cities_light.models import City, Region, Country


class CitationModelTest(TestCase):
    def test_citation_name_string_representation(self):
        person = Person.objects.create()
        name = 'NAME, Citation'
        citation_name = CitationName.objects.create(person=person, name=name)

        self.assertEqual(citation_name.__str__(), name)

    def test_save_new_citation_name_as_default_name_sets_other_citations_names_of_a_person_to_false(self):
        person = Person.objects.create()
        name1 = 'NAME 1, Citation'
        name2 = 'NAME 2, Citation'
        CitationName.objects.create(person=person, name=name1, default_name=True)
        self.assertTrue(CitationName.objects.get(name=name1).default_name)

        CitationName.objects.create(person=person, name=name2, default_name=True)
        self.assertFalse(CitationName.objects.get(name=name1).default_name)
        self.assertTrue(CitationName.objects.get(name=name2).default_name)

    def test_save_new_citation_name_as_default(self):
        person = Person.objects.create()
        name1 = 'NAME 1, Citation'
        name2 = 'NAME 2, Citation'
        CitationName.objects.create(person=person, name=name1)
        self.assertFalse(CitationName.objects.get(name=name1).default_name)

        CitationName.objects.create(person=person, name=name2, default_name=True)
        self.assertFalse(CitationName.objects.get(name=name1).default_name)
        self.assertTrue(CitationName.objects.get(name=name2).default_name)


class InstitutionModelTest(TestCase):
    def test_parent_institution_string_reprentation(self):
        name = 'Fundação de Amparo à Pesquisa do Estado de São Paulo'
        institution = Institution(name=name)

        self.assertEqual(institution.__str__(), name)

    def test_child_institution_string_representation_with_parent_with_acronym(self):
        parent_name = "Fundação de Amparo à Pesquisa do Estado de São Paulo"
        parent_acronym = "FAPESP"
        parent_institution = Institution(name=parent_name, acronym=parent_acronym)
        child_name = "NeuroMat"
        child_institution = Institution(name=child_name, belongs_to=parent_institution)
        self.assertEqual(child_institution.__str__(), child_name + " / " + parent_acronym)

    def test_child_institution_string_representation_with_parent_without_acronym(self):
        parent_name = "Fundação de Amparo à Pesquisa do Estado de São Paulo"
        parent_institution = Institution(name=parent_name)
        child_name = "NeuroMat"
        child_institution = Institution(name=child_name, belongs_to=parent_institution)
        self.assertEqual(child_institution.__str__(), child_name + " / " + parent_name)

    def test_child_institution_string_representation_with_both_parent_and_grand_parent_with_acronym(self):
        grand_parent_name = "Estado de São Paulo"
        grand_parent_acronym = "SP"
        grand_parent_institution = Institution(name=grand_parent_name, acronym=grand_parent_acronym)
        parent_name = "Fundação de Amparo à Pesquisa do Estado de São Paulo"
        parent_acronym = "FAPESP"
        parent_institution = Institution(name=parent_name, acronym=parent_acronym, belongs_to=grand_parent_institution)
        child_name = "NeuroMat"
        child_institution = Institution(name=child_name, belongs_to=parent_institution)
        self.assertEqual(child_institution.__str__(),
                         child_name + " - " + parent_acronym + "/" + grand_parent_acronym)

    def test_child_institution_string_representation_with_parent_with_acronym_and_grand_parent_without_acronym(self):
        grand_parent_name = "Estado de São Paulo"
        grand_parent_institution = Institution(name=grand_parent_name)
        parent_name = "Fundação de Amparo à Pesquisa do Estado de São Paulo"
        parent_acronym = "FAPESP"
        parent_institution = Institution(name=parent_name, acronym=parent_acronym, belongs_to=grand_parent_institution)
        child_name = "NeuroMat"
        child_institution = Institution(name=child_name, belongs_to=parent_institution)
        self.assertEqual(child_institution.__str__(),
                         child_name + " - " + parent_acronym + "/" + grand_parent_name)

    def test_child_institution_string_representation_with_parent_without_acronym_and_grand_parent_with_acronym(self):
        grand_parent_name = "Estado de São Paulo"
        grand_parent_acronym = "SP"
        grand_parent_institution = Institution(name=grand_parent_name, acronym=grand_parent_acronym)
        parent_name = "Fundação de Amparo à Pesquisa do Estado de São Paulo"
        parent_institution = Institution(name=parent_name, belongs_to=grand_parent_institution)
        child_name = "NeuroMat"
        child_institution = Institution(name=child_name, belongs_to=parent_institution)
        self.assertEqual(child_institution.__str__(),
                         child_name + " - " + parent_name + "/" + grand_parent_acronym)

    def test_child_institution_string_representation_with_both_parent_and_grand_parent_without_acronym(self):
        grand_parent_name = "Estado de São Paulo"
        grand_parent_institution = Institution(name=grand_parent_name)
        parent_name = "Fundação de Amparo à Pesquisa do Estado de São Paulo"
        parent_institution = Institution(name=parent_name, belongs_to=grand_parent_institution)
        child_name = "NeuroMat"
        child_institution = Institution(name=child_name, belongs_to=parent_institution)
        self.assertEqual(child_institution.__str__(),
                         child_name + " - " + parent_name + "/" + grand_parent_name)

    def test_person_institution_without_acronym(self):
        name = 'Fundação de Amparo à Pesquisa do Estado de São Paulo'
        institution = Institution(name=name)

        self.assertEqual(institution.get_person_institution(), name)

    def test_person_institution_with_acronym(self):
        name = 'Fundação de Amparo à Pesquisa do Estado de São Paulo'
        acronym = 'FAPESP'
        institution = Institution(name=name, acronym=acronym)

        self.assertEqual(institution.get_person_institution(), acronym)

    def test_person_child_institution_with_acronym_and_parent_with_acronym(self):
        parent_name = "Fundação de Amparo à Pesquisa do Estado de São Paulo"
        parent_acronym = "FAPESP"
        parent_institution = Institution(name=parent_name, acronym=parent_acronym)
        child_name = "Centro de Pesquisa, Inovação e Difusão em Neuromatemática"
        child_acronym = "NeuroMat"
        child_institution = Institution(name=child_name, acronym=child_acronym, belongs_to=parent_institution)
        self.assertEqual(child_institution.get_person_institution(), child_acronym + "-" + parent_acronym)

    def test_person_child_institution_with_acronym_and_parent_without_acronym(self):
        parent_name = "Fundação de Amparo à Pesquisa do Estado de São Paulo"
        parent_institution = Institution(name=parent_name)
        child_name = "Centro de Pesquisa, Inovação e Difusão em Neuromatemática"
        child_acronym = "NeuroMat"
        child_institution = Institution(name=child_name, acronym=child_acronym, belongs_to=parent_institution)
        self.assertEqual(child_institution.get_person_institution(), child_acronym + "-" + parent_name)

    def test_person_child_institution_without_acronym_and_parent_with_acronym(self):
        parent_name = "Fundação de Amparo à Pesquisa do Estado de São Paulo"
        parent_acronym = "FAPESP"
        parent_institution = Institution(name=parent_name, acronym=parent_acronym)
        child_name = "Centro de Pesquisa, Inovação e Difusão em Neuromatemática"
        child_institution = Institution(name=child_name, belongs_to=parent_institution)
        self.assertEqual(child_institution.get_person_institution(), child_name + "-" + parent_acronym)

    def test_person_child_institution_without_acronym_and_parent_without_acronym(self):
        parent_name = "Fundação de Amparo à Pesquisa do Estado de São Paulo"
        parent_institution = Institution(name=parent_name)
        child_name = "Centro de Pesquisa, Inovação e Difusão em Neuromatemática"
        child_institution = Institution(name=child_name, belongs_to=parent_institution)
        self.assertEqual(child_institution.get_person_institution(), child_name + "-" + parent_name)

    def test_person_parent_institution_with_acronym_and_grandparent_with_acronym(self):
        grand_parent_name = "Estado de São Paulo"
        grand_parent_acronym = "SP"
        grand_parent_institution = Institution(name=grand_parent_name, acronym=grand_parent_acronym)
        parent_name = "Fundação de Amparo à Pesquisa do Estado de São Paulo"
        parent_acronym = "FAPESP"
        parent_institution = Institution(name=parent_name, acronym=parent_acronym, belongs_to=grand_parent_institution)
        child_name = "Centro de Pesquisa, Inovação e Difusão em Neuromatemática"
        child_institution = Institution(name=child_name, belongs_to=parent_institution)
        self.assertEqual(child_institution.get_person_institution(),
                         child_name + " - " + parent_acronym + "/" + grand_parent_acronym)

    def test_person_parent_institution_with_acronym_and_grandparent_without_acronym(self):
        grand_parent_name = "Estado de São Paulo"
        grand_parent_institution = Institution(name=grand_parent_name)
        parent_name = "Fundação de Amparo à Pesquisa do Estado de São Paulo"
        parent_acronym = "FAPESP"
        parent_institution = Institution(name=parent_name, acronym=parent_acronym, belongs_to=grand_parent_institution)
        child_name = "Centro de Pesquisa, Inovação e Difusão em Neuromatemática"
        child_institution = Institution(name=child_name, belongs_to=parent_institution)
        self.assertEqual(child_institution.get_person_institution(),
                         child_name + " - " + parent_acronym + "/" + grand_parent_name)

    def test_person_parent_institution_without_acronym_and_grandparent_with_acronym(self):
        grand_parent_name = "Estado de São Paulo"
        grand_parent_acronym = "SP"
        grand_parent_institution = Institution(name=grand_parent_name, acronym=grand_parent_acronym)
        parent_name = "Fundação de Amparo à Pesquisa do Estado de São Paulo"
        parent_institution = Institution(name=parent_name, belongs_to=grand_parent_institution)
        child_name = "Centro de Pesquisa, Inovação e Difusão em Neuromatemática"
        child_institution = Institution(name=child_name, belongs_to=parent_institution)
        self.assertEqual(child_institution.get_person_institution(),
                         child_name + " - " + parent_name + "/" + grand_parent_acronym)

    def test_person_parent_institution_without_acronym_and_grandparent_without_acronym(self):
        grand_parent_name = "Estado de São Paulo"
        grand_parent_institution = Institution(name=grand_parent_name)
        parent_name = "Fundação de Amparo à Pesquisa do Estado de São Paulo"
        parent_institution = Institution(name=parent_name, belongs_to=grand_parent_institution)
        child_name = "Centro de Pesquisa, Inovação e Difusão em Neuromatemática"
        child_institution = Institution(name=child_name, belongs_to=parent_institution)
        self.assertEqual(child_institution.get_person_institution(),
                         child_name + " - " + parent_name + "/" + grand_parent_name)


class InstitutionTypeModelTest(TestCase):
    def test_institution_type_string_representation(self):
        name = 'Fundação'
        institution_type = InstitutionType.objects.create(name=name)

        self.assertEqual(institution_type.__str__(), name)


class RoleModelTest(TestCase):
    def test_role_string_representation(self):
        name = 'Associate Investigator'
        role = Role.objects.create(name=name)

        self.assertEqual(role.__str__(), name)


class PersonModelTest(TestCase):

    def test_person_string_reprentation(self):
        full_name = 'Nildo'
        person = Person.objects.create(full_name=full_name)

        self.assertEqual(person.__str__(), full_name)

    def test_save_email_in_person_instance_without_user_instance(self):
        person = Person.objects.create()
        email = "test@email.model"
        person.email = email
        person.save()

        user = User.objects.filter(user_profile=person.pk).first()
        self.assertIsNone(user)
        self.assertEqual(person.email, email)

    def test_save_email_in_person_instance_with_user_instance(self):
        person = Person.objects.create()
        user = User.objects.create()
        user.user_profile = person
        user.save()
        self.assertIsNone(User.objects.first().email)

        email = "test@email.model"
        person.email = email
        person.save()

        self.assertEqual(User.objects.first().email, email)


class CPFValidation(TestCase):
    def test_validation_of_cpf_fails_with_dummy_cpf(self):
        value = '00000000000'
        with self.assertRaises(ValidationError) as cm:
            validate_cpf(value).full_clean()
        self.assertEqual(ValidationError('%s is not a valid CPF' % value).message, cm.exception.message)

    def test_validation_of_cpf_success_with_valid_cpf(self):
        value = '40796346097'
        self.assertIsNone(validate_cpf(value))


class PersonAppIntegration(TestCase):
    def test_do_not_delete_institution_type_instance_if_there_is_institution_associated(self):
        self.assertEqual(InstitutionType.objects.count(), 0)
        self.assertEqual(Institution.objects.count(), 0)

        institution_type = InstitutionType.objects.create(name='InstitutionType_Test')
        institution = Institution.objects.create(name='Institution_Test', type=institution_type)

        with self.assertRaises(ProtectedError) as e:
            institution_type.delete()

        self.assertEqual(InstitutionType.objects.last(), institution_type)
        self.assertEqual(Institution.objects.last(), institution)

    def test_do_not_delete_institution_instance_if_there_is_a_child_institution_associated(self):
        self.assertEqual(InstitutionType.objects.count(), 0)
        self.assertEqual(Institution.objects.count(), 0)

        institution_type = InstitutionType.objects.create(name='InstitutionType_Test')
        institution_parent = Institution.objects.create(name='Institution_Parent_Test', type=institution_type)
        institution_child = Institution.objects.create(
            name='Institution_Child_Test',
            type=institution_type,
            belongs_to=institution_parent)

        with self.assertRaises(ProtectedError) as e:
            institution_parent.delete()

        self.assertEqual(InstitutionType.objects.last(), institution_type)
        self.assertEqual(Institution.objects.last(), institution_parent)
        self.assertEqual(Institution.objects.first(), institution_child)

    def test_do_not_delete_institution_instance_if_there_is_a_person_associated(self):
        self.assertEqual(InstitutionType.objects.count(), 0)
        self.assertEqual(Institution.objects.count(), 0)
        self.assertEqual(Person.objects.count(), 0)

        institution_type = InstitutionType.objects.create(name='InstitutionType_Test')
        institution = Institution.objects.create(name='Institution_Parent_Test', type=institution_type)
        person = Person.objects.create(full_name='Person_Test', institution=institution)

        with self.assertRaises(ProtectedError) as e:
            institution.delete()

        self.assertEqual(InstitutionType.objects.last(), institution_type)
        self.assertEqual(Institution.objects.last(), institution)
        self.assertEqual(Person.objects.last(), person)

    def test_do_not_delete_city_instance_if_there_is_institution_associated(self):
        self.assertEqual(Country.objects.count(), 0)
        self.assertEqual(City.objects.count(), 0)
        self.assertEqual(InstitutionType.objects.count(), 0)
        self.assertEqual(Institution.objects.count(), 0)

        country = Country.objects.create(name='Brazil')
        city = City.objects.create(name='São Paulo', country=country)

        institution_type = InstitutionType.objects.create(name='InstitutionType_Test')
        institution = Institution.objects.create(name='Institution_Parent_Test', type=institution_type, city=city)

        with self.assertRaises(ProtectedError) as e:
            city.delete()

        self.assertEqual(Country.objects.last(), country)
        self.assertEqual(City.objects.last(), city)
        self.assertEqual(InstitutionType.objects.last(), institution_type)
        self.assertEqual(Institution.objects.last(), institution)

    def test_do_not_delete_role_instance_if_there_is_person_associated(self):
        self.assertEqual(Role.objects.count(), 0)
        self.assertEqual(Person.objects.count(), 0)

        role = Role.objects.create(name='Role_Test')
        person = Person.objects.create(full_name='Person', role=role)

        with self.assertRaises(ProtectedError) as e:
            role.delete()

        self.assertEqual(Role.objects.last(), role)
        self.assertEqual(Person.objects.last(), person)

    def test_delete_person_instance_associated_with_citation_names_delete_them(self):
        self.assertEqual(Person.objects.count(), 0)
        self.assertEqual(CitationName.objects.count(), 0)

        person = Person.objects.create(full_name='Person')
        citation_name_1 = CitationName.objects.create(name='C.I.T.A.T.I.O.N, Person', person=person, default_name=True)
        citation_name_2 = CitationName.objects.create(name='C.I.T.A.T.I.O.N, P.', person=person, default_name=False)

        self.assertEqual(Person.objects.last(), person)
        self.assertEqual(CitationName.objects.all()[0], citation_name_1)
        self.assertEqual(CitationName.objects.all()[1], citation_name_2)

        person.delete()

        self.assertEqual(Person.objects.count(), 0)
        self.assertEqual(CitationName.objects.count(), 0)
