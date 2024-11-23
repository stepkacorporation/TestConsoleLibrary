from unittest import TestCase

from app.library import BookStatus


class TestBookStatus(TestCase):

    def test_enum_values(self):
        self.assertEqual(BookStatus.IN_STOCK.value, 'в наличии')
        self.assertEqual(BookStatus.BORROWED.value, 'выдана')

    def test_values_method(self):
        expected_values = ['в наличии', 'выдана']
        self.assertEqual(BookStatus.values(), expected_values)

    def test_from_value_valid(self):
        self.assertEqual(BookStatus.from_value('в наличии'), BookStatus.IN_STOCK)
        self.assertEqual(BookStatus.from_value('выдана'), BookStatus.BORROWED)

    def test_from_value_case_insensitive(self):
        self.assertEqual(BookStatus.from_value('В НАЛИЧИи'), BookStatus.IN_STOCK)
        self.assertEqual(BookStatus.from_value('выДанА'), BookStatus.BORROWED)

    def test_from_value_invalid(self):
        with self.assertRaises(ValueError) as context:
            BookStatus.from_value('неизвестно')
        self.assertIn('Неверное значение', str(context.exception))
        self.assertIn('в наличии', str(context.exception))
        self.assertIn('выдана', str(context.exception))

    def test_from_value_empty_string(self):
        with self.assertRaises(ValueError):
            BookStatus.from_value('')
