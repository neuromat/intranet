from django.test import TestCase
from validation import CPF


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