# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from person.models import Person, CitationName
from person.views import name_with_first_letters, names_without_last_name, first_name_and_first_letter, \
    generate_citation_names
from person.validation import CPF

prep = ['e', 'da', 'do', 'de', 'dos', 'E', 'Da', 'Do', 'De', 'Dos']


class CpfValidationTest(TestCase):

    """
    The following tests are performed:
    1 - Valid CPFs with dot and dash;
    2 - Valid CPFs, only numbers;
    3 - Invalid CPFs with dot and dash;
    4 - Invalid CPFs, only numbers;
    6 - CPF with repeated numbers;
    5 - CPF with letters;
    6 - CPF with special character;
    7 - CPF with long string.
    """

    good_values = (
        '288.666.827-30',
        '597.923.110-25',
        '981.108.954-09',
        '174.687.414-76',
        '774.321.431-10',
    )

    good_only_numbers = (
        '28866682730',
        '59792311025',
        '98110895409',
        '17468741476',
        '77432143110',
    )

    bad_values = (
        '288.666.827-31',
        '597.923.110-26',
        '981.108.954-00',
        '174.687.414-77',
        '774.321.431-11',
    )

    bad_only_numbers = (
        '28866682731',
        '59792311026',
        '98110895400',
        '17468741477',
        '77432143111',
    )

    invalid_values = (
        '00000000000',
        '11111111111',
        '22222222222',
        '33333333333',
        '44444444444',
        '55555555555',
        '66666666666',
        '77777777777',
        '88888888888',
        '99999999999'
    )

    def test_good_values(self):
        for cpf in self.good_values:
            result = CPF(cpf).isValid()
            self.assertEqual(result, True)

    def test_good_only_numbers(self):
        for cpf in self.good_only_numbers:
            result = CPF(cpf).isValid()
            self.assertEqual(result, True)

    def test_bad_values(self):
        for cpf in self.bad_values:
            result = CPF(cpf).isValid()
            self.assertEqual(result, False)

    def test_bad_only_numbers(self):
        for cpf in self.bad_only_numbers:
            result = CPF(cpf).isValid()
            self.assertEqual(result, False)

    def test_invalid_values(self):
        for cpf in self.invalid_values:
            result = CPF(cpf).isValid()
            self.assertEqual(result, False)

    def test_letter(self):
        result = CPF('111.ABC').isValid()
        self.assertEqual(result, False)

    def test_special_character(self):
        result = CPF('!@#$%&*()-_=+[]|"?><;:').isValid()
        self.assertEqual(result, False)

    def test_long_string(self):
        result = CPF(
            '1234567890123456789012345678901234567890123456789012\
            34567890123456789012345678901234567890123456789012345678901234567890').isValid()
        self.assertEqual(result, False)


class CitationsTest(TestCase):

    def setUp(self):
        self.person1 = Person(full_name='João Carlos da Silva')
        self.person1.save()

        self.person2 = Person(full_name='Antonio da Silva')
        self.person2.save()

        self.person1_id = self.person1.pk
        self.person2_id = self.person2.pk

        citation2 = CitationName(person_id=self.person2_id, name='da Silva, A', default_name=True)
        citation2.save()

    def test_name_with_first_letters(self):

        result = name_with_first_letters(self.person1.full_name.split(), False)
        self.assertEqual(result, 'Silva, JC')

        result = name_with_first_letters(self.person1.full_name.split(), True)
        self.assertEqual(result, 'da Silva, JC')

    def test_names_without_last_name(self):

        result = names_without_last_name(self.person1.full_name.split(), False)
        self.assertEqual(result, 'Silva, João Carlos')

        result = names_without_last_name(self.person1.full_name.split(), True)
        self.assertEqual(result, 'da Silva, João Carlos')

    def test_first_name_and_first_letter(self):

        result = first_name_and_first_letter(self.person1.full_name.split(), False)
        self.assertEqual(result, 'Silva, João C')

        result = first_name_and_first_letter(self.person1.full_name.split(), True)
        self.assertEqual(result, 'da Silva, João C')

    def test_generate_citation_names(self):

        for person in Person.objects.all():
            generate_citation_names(person)

        citation = CitationName.objects.filter(person_id=self.person1_id, default_name=True)
        self.assertEqual('Silva, JC', citation[0].name)

        citation = CitationName.objects.filter(person_id=self.person2_id, default_name=True)
        self.assertEqual('da Silva, A', citation[0].name)

    def test_citation_names(self):
        response = self.client.get(reverse('citation_names'))
        self.assertEqual(response.status_code, 302)