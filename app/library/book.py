# P.S. Для валидации я бы использовал модели pydantic, ну либо так :)

import re

from datetime import datetime, timezone
from enum import Enum

from app.utils import get_int_input, get_str_input, handle_input_errors


class BookStatus(Enum):
    """Перечисление для статусов книги."""

    IN_STOCK = 'в наличии'
    BORROWED = 'выдана'

    @classmethod
    def values(cls) -> list[str]:
        """
        Возвращает список всех возможных значений статусов книги.

        Returns:
            list[str]: Список строковых представлений статусов.

        Example:
            >>> BookStatus.values()
            ['в наличии', 'выдана']
        """

        return [status.value for status in cls]

    @classmethod
    def from_value(cls, value: str) -> 'BookStatus':
        """
        Конвертирует строковое значение в соответствующий элемент BookStatus.

        Args:
            value (str): Строковое значение статуса книги (например, 'в наличии').

        Raises:
            ValueError: Если переданное значение не соответствует ни одному статусу.

        Returns:
            BookStatus: Соответствующий элемент перечисления BookStatus.

        Example:
            >>> BookStatus.from_value('в наличии')
            <BookStatus.IN_STOCK: 'в наличии'>
        """

        value = value.lower()
        for status in cls:
            if status.value.lower() == value:
                return status
        raise ValueError(f'Неверное значение: \'{value}\'. Допустимые значения: {", ".join(cls.values())}')


class Book:
    """
    Класс, представляющий книгу в библиотеке.

    Attributes:
        MIN_YEAR (int): Минимально допустимый год издания книги.
        MIN_TITLE_LENGTH (int): Минимальная длина названия книги.
        MAX_TITLE_LENGTH (int): Максимальная длина названия книги.
        MIN_AUTHOR_LENGTH (int): Минимальная длина имени автора.
        MAX_AUTHOR_LENGTH (int): Максимальная длина имени автора.
    """

    MIN_YEAR = 1000
    MIN_TITLE_LENGTH = 2
    MAX_TITLE_LENGTH = 50
    MIN_AUTHOR_LENGTH = 2
    MAX_AUTHOR_LENGTH = 25

    def __init__(self, id_: int, title: str, author: str, year: int, status: BookStatus):
        """
        Инициализация нового объекта книги.

        Args:
            id_ (int): Уникальный идентификатор книги.
            title (str): Название книги
            author (str): Автор книги.
            year (int): Год издания книги.
            status (BookStatus): Статус книги. Должен быть одним из значения перечисления `BookStatus`.

        Raises:
            ValueError: Если какой-либо из параметров не проходит валидацию.
        """

        self.id = self.validate_id(id_)
        self.title = self.validate_title(title)
        self.author = self.validate_author(author)
        self.year = self.validate_year(year)
        self.status = self.validate_status(status)

    def __repr__(self):
        """
        Возвращает строковое представление объекта книги для отладки.

        Returns:
            str: Представление книги в формате: Book(id, title, author, year, status).
        """

        return f'{self.__class__.__name__}({self.id}, {self.title}, {self.author}, {self.year}, {self.status})'

    def to_dict(self) -> dict:
        """
        Преобразует объект книги в словарь.

        Returns:
            dict: Словарь, представляющий книгу.

        Example:
            >>> book = Book(1, "Война и мир", "Л. Толстой", 1869, BookStatus.IN_STOCK)
            >>> book.to_dict()
            {
                'id': 1,
                'title': 'Война и мир',
                'author': 'Л. Толстой',
                'year': 1869,
                'status': 'в наличии'
            }
        """

        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status.value
        }

    @staticmethod
    def validate_id(id_: int) -> int:
        """
        Проверка валидности идентификатора книги.

        Args:
            id_ (int): Идентификатор книги.

        Raises:
            ValueError: Если id не является положительным целым числом.

        Returns:
            int: Валидный идентификатор книги.
        """

        if not isinstance(id_, int) or id_ < 1:
            raise ValueError('ID книги должен быть положительным целым числом')
        return id_

    @classmethod
    def validate_title(cls, title: str) -> str:
        """
        Проверка валидности названия книги.

        Args:
            title (str): Название книги.

        Raises:
            ValueError: Если название пустое или не строка.

        Returns:
            str: Валидное название книги.
        """

        title = title.strip()
        if not title or not isinstance(title, str):
            raise ValueError('Название книги должно быть непустой строкой')
        if not (cls.MIN_TITLE_LENGTH <= len(title) <= cls.MAX_TITLE_LENGTH):
            raise ValueError(f'Название книги должно быть длиной от {cls.MIN_TITLE_LENGTH}'
                             f' до {cls.MAX_TITLE_LENGTH} символов')
        return title

    @classmethod
    def validate_author(cls, author: str) -> str:
        """
        Проверка валидности имени автора.

        Args:
            author (str): Имя автора книги.

        Raises:
            ValueError: Если имя автора пустое, не строка или содержит недопустимые символы.

        Returns:
            str: Валидное имя автора.
        """

        author = author.strip()
        if not author or not isinstance(author, str):
            raise ValueError('Имя автора должно быть непустой строкой')
        if not (cls.MIN_AUTHOR_LENGTH <= len(author) <= cls.MAX_AUTHOR_LENGTH):
            raise ValueError(f'Имя автора должно быть длиной от {cls.MIN_AUTHOR_LENGTH} '
                             f'до {cls.MAX_AUTHOR_LENGTH} символов')
        if not re.fullmatch(r'^[А-ЯЁа-яёA-Za-z\s.]+$', author):
            raise ValueError('Имя автора может содержать только буквы, пробелы и точки')
        return author

    @classmethod
    def validate_year(cls, year: int) -> int:
        """
        Проверка валидности года издания книги.

        Args:
            year (int): Год издания книги.

        Raises:
            ValueError: Если год не целое число или не находится в допустимом диапазоне.

        Returns:
            int: Валидный год издания книги.
        """

        current_year = datetime.now(timezone.utc).year
        if not isinstance(year, int) or not (cls.MIN_YEAR <= year <= current_year):
            raise ValueError(f'Год издания должен быть целым числом в диапазоне'
                             f' от {cls.MIN_YEAR} до {current_year} включительно')
        return year

    @classmethod
    def validate_status(cls, status: BookStatus) -> BookStatus:
        """
        Проверка валидности статуса книги.

        Args:
            status (str): Статус книги.

        Raises:
            ValueError: Если статус не является одним из допустимых значений.

        Returns:
            str: Валидный статус книги.
        """

        if not isinstance(status, BookStatus):
            raise ValueError(f'Статус книги должен быть одним из следующих: {tuple(BookStatus.values())}')
        return status


class BookInterface:
    """
    Вспомогательный интерфейс для ввода данных о книге.

    Методы предоставляют безопасный ввод данных с использованием встроенной валидации класса Book
    и обрабатывают ошибки ввода через декоратор `@handle_input_errors`.
    """

    @staticmethod
    @handle_input_errors
    def input_id(prompt: str = 'Введите ID книги: ') -> int:
        """
        Ввод идентификатора книги с валидацией.

        Args:
            prompt (str): Сообщение для пользователя. По умолчанию: 'Введите ID книги: '.

        Returns:
            int: Валидный идентификатор книги.
        """

        return Book.validate_id(get_int_input(prompt))

    @staticmethod
    @handle_input_errors
    def input_title(prompt: str = 'Введите название книги: ') -> str:
        """
        Ввод названия книги с валидацией.

        Args:
            prompt (str): Сообщение для пользователя. По умолчанию: 'Введите название книги: '.

        Returns:
            str: Валидное название книги.
        """

        return Book.validate_title(get_str_input(prompt))

    @staticmethod
    @handle_input_errors
    def input_author(prompt: str = 'Введите автора книги: ') -> str:
        """
        Ввод имени автора с валидацией.

        Args:
            prompt (str): Сообщение для пользователя. По умолчанию: 'Введите автора книги: '.

        Returns:
            str: Валидное имя автора.
        """

        return Book.validate_author(get_str_input(prompt))

    @staticmethod
    @handle_input_errors
    def input_year(prompt: str = 'Введите год издания книги: ') -> int:
        """
        Ввод года издания книги с валидацией.

        Args:
            prompt (str): Сообщение для пользователя. По умолчанию: 'Введите год издания книги: '.

        Returns:
            int: Валидный год издания книги.
        """

        return Book.validate_year(get_int_input(prompt))

    @staticmethod
    @handle_input_errors
    def input_status(prompt: str | None = None) -> BookStatus:
        """
        Ввод статуса книги с валидацией.

        Args:
            prompt (str | None): Сообщение для пользователя. Если не указано, будет использовано значение по умолчанию.

        Returns:
            BookStatus: Валидный статус книги.
        """

        statuses = BookStatus.values()
        prompt = f'Введите статус книги ({", ".join(statuses)})' if prompt is None else prompt
        status_input = get_str_input(prompt, valid_values=statuses)
        return Book.validate_status(BookStatus.from_value(status_input))
