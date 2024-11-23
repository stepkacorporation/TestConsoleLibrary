from unittest import TestCase
from unittest.mock import patch

from app.library import BookInterface, BookStatus


class TestBookInterface(TestCase):

    # Тест ввода ID
    @patch('builtins.input', side_effect=['10'])
    def test_input_id_valid(self, mock_input):
        self.assertEqual(BookInterface.input_id('Введите ID книги: '), 10)

    @patch('builtins.input', side_effect=['-1', '10'])
    def test_input_id_invalid_then_valid(self, mock_input):
        self.assertEqual(BookInterface.input_id('Введите ID книги: '), 10)

    @patch('builtins.input', side_effect=['0', '10'])
    def test_input_id_zero_then_valid(self, mock_input):
        self.assertEqual(BookInterface.input_id('Введите ID книги: '), 10)

    # Тест ввода названия книги
    @patch('builtins.input', side_effect=['Преступление и наказание'])
    def test_input_title_valid(self, mock_input):
        self.assertEqual(BookInterface.input_title('Введите название книги: '), 'Преступление и наказание')

    @patch('builtins.input', side_effect=['', 'Преступление и наказание'])
    def test_input_title_empty_then_valid(self, mock_input):
        self.assertEqual(BookInterface.input_title('Введите название книги: '), 'Преступление и наказание')

    # Тест ввода автора книги
    @patch('builtins.input', side_effect=['Достоевский'])
    def test_input_author_valid(self, mock_input):
        self.assertEqual(BookInterface.input_author('Введите автора книги: '), 'Достоевский')

    @patch('builtins.input', side_effect=['', 'Достоевский'])
    def test_input_author_empty_then_valid(self, mock_input):
        self.assertEqual(BookInterface.input_author('Введите автора книги: '), 'Достоевский')

    # Тест ввода года издания
    @patch('builtins.input', side_effect=['2000'])
    def test_input_year_valid(self, mock_input):
        self.assertEqual(BookInterface.input_year('Введите год издания книги: '), 2000)

    @patch('builtins.input', side_effect=['2300', '2000'])
    def test_input_year_invalid_then_valid(self, mock_input):
        self.assertEqual(BookInterface.input_year('Введите год издания книги: '), 2000)

    @patch('builtins.input', side_effect=['999', '1000'])
    def test_input_year_too_early_then_valid(self, mock_input):
        self.assertEqual(BookInterface.input_year('Введите год издания книги: '), 1000)

    @patch('builtins.input', side_effect=['999', '2300', '2020'])
    def test_input_year_multiple_invalid_then_valid(self, mock_input):
        self.assertEqual(BookInterface.input_year('Введите год издания книги: '), 2020)

    # Тест ввода статуса книги
    @patch('builtins.input', side_effect=['выдана'])
    def test_input_status_valid(self, mock_input):
        self.assertEqual(BookInterface.input_status('Введите статус книги: '), BookStatus.BORROWED)

    @patch('builtins.input', side_effect=['неверный статус', 'в наличии'])
    def test_input_status_invalid_then_valid(self, mock_input):
        self.assertEqual(BookInterface.input_status('Введите статус книги: '), BookStatus.IN_STOCK)

    @patch('builtins.input', side_effect=['в наличии'])
    def test_input_status_default_prompt(self, mock_input):
        self.assertEqual(BookInterface.input_status(), BookStatus.IN_STOCK)
