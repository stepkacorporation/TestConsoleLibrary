import os
from unittest import TestCase
from unittest.mock import patch, MagicMock

from app.library import Library, BookStatus


class TestLibrary(TestCase):

    def setUp(self):
        self.lib = Library('test_library.json')

    def tearDown(self):
        if os.path.exists(self.lib._storage):
            os.remove(self.lib._storage)

    @patch('builtins.open', new_callable=MagicMock)
    def test_initialization_valid_storage(self, mock_open):
        self.assertEqual(self.lib._storage, 'test_library.json')

    def test_add_book_valid(self):
        self.lib.add_book('Title', 'Author', 2000)
        self.assertEqual(len(self.lib._books), 1)

    def test_delete_book_valid(self):
        self.lib.add_book('Title', 'Author', 2000)
        book_id = self.lib._books[0].id
        self.lib.delete_book(book_id)
        self.assertEqual(len(self.lib._books), 0)

    def test_delete_book_invalid(self):
        with self.assertRaises(ValueError):
            self.lib.delete_book(999)

    def test_search_books_valid(self):
        self.lib.add_book('Title', 'Author', 2000)
        results = self.lib.search_books('title', 'title')
        self.assertEqual(len(results), 1)

    def test_search_books_invalid_field(self):
        with self.assertRaises(ValueError):
            self.lib.search_books('title', 'invalid')

    def test_change_status_valid(self):
        self.lib.add_book('Title', 'Author', 2000)
        book_id = self.lib._books[0].id
        self.lib.change_status(book_id, BookStatus.IN_STOCK)
        self.assertEqual(self.lib._books[0].status, BookStatus.IN_STOCK)

    def test_save_books(self):
        self.lib.add_book('Title', 'Author', 2000)
        with patch('builtins.open', new_callable=MagicMock) as mock_open:
            self.lib._save_books()
            mock_open.assert_called_once_with('test_library.json', 'w', encoding='utf-8')
