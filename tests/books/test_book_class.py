from unittest import TestCase
from datetime import datetime, timezone

from app.library import Book, BookStatus


class TestBook(TestCase):
    def setUp(self):
        self.valid_id = 1
        self.valid_title = 'Война и мир'
        self.valid_author = 'Толстой Л.Н.'
        self.valid_year = 1869
        self.valid_status = BookStatus.IN_STOCK

    # Тесты для конструктора
    def test_book_initialization_valid(self):
        book = Book(self.valid_id, self.valid_title, self.valid_author, self.valid_year, self.valid_status)
        self.assertEqual(book.id, self.valid_id)
        self.assertEqual(book.title, self.valid_title)
        self.assertEqual(book.author, self.valid_author)
        self.assertEqual(book.year, self.valid_year)
        self.assertEqual(book.status, self.valid_status)

    # Тесты для validate_id
    def test_validate_id_valid(self):
        self.assertEqual(Book.validate_id(1), 1)

    def test_validate_id_invalid_negative(self):
        with self.assertRaises(ValueError):
            Book.validate_id(-1)

    def test_validate_id_invalid_zero(self):
        with self.assertRaises(ValueError):
            Book.validate_id(0)

    def test_validate_id_invalid_non_int(self):
        with self.assertRaises(ValueError):
            Book.validate_id('1')

    # Тесты для validate_title
    def test_validate_title_valid(self):
        self.assertEqual(Book.validate_title('Гарри Поттер'), 'Гарри Поттер')

    def test_validate_title_invalid_too_short(self):
        with self.assertRaises(ValueError):
            Book.validate_title('A')

    def test_validate_title_invalid_too_long(self):
        with self.assertRaises(ValueError):
            Book.validate_title('A' * 51)

    def test_validate_title_invalid_empty(self):
        with self.assertRaises(ValueError):
            Book.validate_title('')

    def test_validate_title_invalid_whitespace(self):
        with self.assertRaises(ValueError):
            Book.validate_title('   ')

    def test_validate_title_invalid_non_string(self):
        with self.assertRaises(ValueError):
            Book.validate_title(123)

    # Тесты для validate_author
    def test_validate_author_valid(self):
        self.assertEqual(Book.validate_author('Л. Толстой'), 'Л. Толстой')

    def test_validate_author_invalid_too_short(self):
        with self.assertRaises(ValueError):
            Book.validate_author('A')

    def test_validate_author_invalid_too_long(self):
        with self.assertRaises(ValueError):
            Book.validate_author('A' * 26)

    def test_validate_author_invalid_empty(self):
        with self.assertRaises(ValueError):
            Book.validate_author('')

    def test_validate_author_invalid_non_string(self):
        with self.assertRaises(ValueError):
            Book.validate_author(123)

    def test_validate_author_invalid_symbols(self):
        with self.assertRaises(ValueError):
            Book.validate_author('Толстой@')

    # Тесты для validate_year
    def test_validate_year_valid(self):
        self.assertEqual(Book.validate_year(1869), 1869)

    def test_validate_year_invalid_too_old(self):
        with self.assertRaises(ValueError):
            Book.validate_year(999)

    def test_validate_year_invalid_future(self):
        future_year = datetime.now(timezone.utc).year + 1
        with self.assertRaises(ValueError):
            Book.validate_year(future_year)

    def test_validate_year_invalid_non_int(self):
        with self.assertRaises(ValueError):
            Book.validate_year('1869')

    # Тесты для validate_status
    def test_validate_status_valid(self):
        self.assertEqual(Book.validate_status(BookStatus.IN_STOCK), BookStatus.IN_STOCK)

    def test_validate_status_invalid(self):
        with self.assertRaises(ValueError):
            Book.validate_status('в наличии')

    # Тесты для __repr__
    def test_repr(self):
        book = Book(self.valid_id, self.valid_title, self.valid_author, self.valid_year, self.valid_status)
        self.assertEqual(
            repr(book),
            f'Book({self.valid_id}, {self.valid_title},'
            f' {self.valid_author}, {self.valid_year}, {self.valid_status})'
        )

    # Тесты для to_dict
    def test_to_dict(self):
        book = Book(self.valid_id, self.valid_title, self.valid_author, self.valid_year, self.valid_status)
        expected_dict = {
            'id': self.valid_id,
            'title': self.valid_title,
            'author': self.valid_author,
            'year': self.valid_year,
            'status': self.valid_status.value
        }
        self.assertEqual(book.to_dict(), expected_dict)