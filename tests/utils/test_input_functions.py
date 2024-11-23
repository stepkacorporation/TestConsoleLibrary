from unittest import TestCase
from unittest.mock import patch

from app.utils import get_int_input, get_str_input


class TestInputFunctions(TestCase):

    # Тесты get_int_input
    def test_get_int_input_valid(self):
        with patch('builtins.input', side_effect=['42']):
            self.assertEqual(get_int_input('Введите число: '), 42)

    def test_get_int_input_invalid_then_valid(self):
        with patch('builtins.input', side_effect=['abc', '42']):
            self.assertEqual(get_int_input('Введите число: '), 42)

    def test_get_int_input_valid_with_constraints(self):
        with patch('builtins.input', side_effect=['3']):
            self.assertEqual(get_int_input('Введите число: ', valid_values=[1, 2, 3]), 3)

    def test_get_int_input_invalid_value(self):
        with patch('builtins.input', side_effect=['5', '3']):
            self.assertEqual(get_int_input('Введите число: ', valid_values=[1, 2, 3]), 3)

    def test_get_int_input_negative(self):
        with patch('builtins.input', side_effect=['-10']):
            self.assertEqual(get_int_input('Введите число: '), -10)

    # Тесты get_str_input
    def test_get_str_input_valid(self):
        with patch('builtins.input', side_effect=['hello']):
            self.assertEqual(get_str_input('Введите строку: '), 'hello')

    def test_get_str_input_invalid_then_valid(self):
        with patch('builtins.input', side_effect=['invalid', 'yes']):
            self.assertEqual(get_str_input('Введите строку: ', valid_values=['yes', 'no']), 'yes')

    def test_get_str_input_valid_with_constraints(self):
        with patch('builtins.input', side_effect=['no']):
            self.assertEqual(get_str_input('Введите строку: ', valid_values=['yes', 'no']), 'no')

    def test_get_str_input_empty_valid(self):
        with patch('builtins.input', side_effect=['']):
            self.assertEqual(get_str_input('Введите строку: '), '')

    def test_get_str_input_case_sensitivity(self):
        with patch('builtins.input', side_effect=['Yes', 'yes']):
            self.assertEqual(get_str_input('Введите строку: ', valid_values=['yes', 'no']), 'yes')

    def test_get_int_input_multiple_invalid_then_valid(self):
        with patch('builtins.input', side_effect=['text', '123abc', '42']):
            self.assertEqual(get_int_input('Введите число: '), 42)

    def test_get_str_input_whitespace_handling(self):
        with patch('builtins.input', side_effect=['   hello   ']):
            self.assertEqual(get_str_input('Введите строку: '), 'hello')
