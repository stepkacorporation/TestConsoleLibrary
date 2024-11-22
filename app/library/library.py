import json

from .book import Book, BookStatus


class Library:
    """Класс, управляющий операциями библиотеки."""

    SEARCH_FIELDS = ('title', 'author', 'year')

    def __init__(self, storage: str = 'library.json'):
        """
        Инициализация библиотеки.

        Args:
            storage (str, optional): Путь к файлу для хранения данных библиотеки (по умолчанию 'library.json').
        """

        self._storage = self._validate_storage(storage)
        self._books: list[Book] = []
        self._last_id = 0
        self._load_books()

    @staticmethod
    def _validate_storage(storage: str) -> str:
        """
        Валидирует путь к файлу для хранения данных библиотеки.

        Args:
            storage (str): Путь к файлу.

        Raises:
            ValueError: Если путь к файлу не является строкой или не имеет расширение .json.

        Returns:
            str: Валидированный путь к файлу.
        """

        if not isinstance(storage, str):
            raise ValueError('Путь к файлу должен быть строкой')

        if not storage.lower().endswith('.json'):
            raise ValueError('Файл для хранения данных должен иметь расширение .json')

        return storage

    def _load_books(self) -> None:
        """
        Загружает книги из JSON-файла.

        Загружает список книг и последний используемый ID из файла, если файл существует.
        В случае ошибок при загрузке или отсутствии файла сбрасывает данные.
        """

        try:
            with open(self._storage, 'r', encoding='utf-8') as file:
                data: dict = json.load(file)
                self._last_id = data.get('last_id', 0)
                books_data = data.get('books', [])
                for book_data in books_data:
                    try:
                        book = Book(
                            id_=book_data.get('id'),
                            title=book_data.get('title'),
                            author=book_data.get('author'),
                            year=book_data.get('year'),
                            status=BookStatus.from_value(book_data.get('status'))
                        )
                        self._append_book_to_list(book)
                    except ValueError as e:
                        print(f'Ошибка при загрузке книги: {book_data} - {e}')
        except (FileNotFoundError, json.JSONDecodeError):
            self._books = []
            self._last_id = 0

    def _save_books(self) -> None:
        """
        Сохраняет книги в JSON-файл.

        Сохраняет текущий список книг и последний используемый ID в файл.
        """

        data = {
            'last_id': self._last_id,
            'books': [book.to_dict() for book in self._books]
        }

        with open(self._storage, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def _append_book_to_list(self, book: Book) -> None:
        """
        Добавляет книгу в список книг и обновляет last_id.

        Проверяет, не существует ли уже книга с таким же ID.

        Args:
            book (Book): Книга для добавления.

        Raises:
            ValueError: Если книга с таким ID уже существует.
        """

        if any(existing_book.id == book.id for existing_book in self._books):
            raise ValueError(f'Книга с ID {book.id} уже существует')
        self._books.append(book)
        self._last_id = max(self._last_id, book.id)

    def _remove_book_from_list(self, book: Book) -> None:
        """
        Удаляет книгу из списка книг.

        Args:
            book (Book): Книга для удаления.

        Raises:
            ValueError: Если книга не найдена в списке.
        """

        try:
            self._books.remove(book)
        except ValueError:
            raise ValueError(f'Книга {book} не найдена в библиотеке')

    def _find_book_by_id(self, book_id: int) -> Book | None:
        """
        Ищет книгу по ID.

        Args:
            book_id (int): ID книги для поиска.

        Returns:
            Book | None: Найденная книга или None, если книга не найдена.
        """

        return next((book for book in self._books if book.id == book_id), None)

    def add_book(self, title: str, author: str, year: int) -> None:
        """
        Добавляет книгу в библиотеку.

        Создает новый объект книги с указанными параметрами и добавляет его в список.

        Args:
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания книги.
        """

        book_id = self._last_id + 1
        try:
            new_book = Book(book_id, title, author, year, BookStatus.IN_STOCK)
            self._append_book_to_list(new_book)
            self._save_books()
            print(f'Книга \'{title}\' успешно добавлена.')
        except ValueError as e:
            print(f'Не удалось добавить книгу: {e}')

    def delete_book(self, book_id: int) -> None:
        """
        Удаляет книгу из библиотеки по ID.

        Ищет книгу по ID, если книга найдена, она удаляется из списка.

        Args:
            book_id (int): ID книги для удаления.
        """

        book = self._find_book_by_id(book_id)
        if book:
            self._remove_book_from_list(book)
            self._save_books()
            print(f'Книга с ID {book_id} успешно удалена')
        else:
            print(f'Книга с ID {book_id} не найдена')

    def search_books(self, keyword: str, field: str) -> list[Book]:
        """
        Ищет книги по указанному полю.

        Фильтрует книги по полю, которое указано в аргументе `field`,
        проверяя, содержит ли значение поля переданное ключевое слово.

        Args:
            keyword (str): Ключевое слово для поиска.
            field (str): Поле для поиска (например, 'title', 'author', 'year').

        Raises:
            ValueError: Если указано недопустимое поле для поиска.

        Returns:
            list[Book]: Список книг, соответствующих поисковому запросу.
        """

        if field not in self.SEARCH_FIELDS:
            raise ValueError(f'Недопустимое поле для поиска. Допустимые значения: {self.SEARCH_FIELDS}')

        result = [book for book in self._books if keyword.lower() in str(getattr(book, field)).lower()]
        return result

    def list_books(self) -> None:
        """
        Отображает список всех книг.

        Если в библиотеке нет книг, выводит сообщение об этом.
        В противном случае вызывает метод отображения книг.
        """

        if not self._books:
            print('В библиотеке пока нет книг.')
        else:
            self.display_books(self._books)

    @staticmethod
    def display_books(books: list[Book]) -> None:
        """
        Выводит список книг в табличной форме.

        Отображает информацию о каждой книге в формате таблицы.

        Args:
            books (list[Book]): Список книг для отображения.
        """

        if not books:
            print('Нет книг для отображения.')
            return

        id_width = 7
        title_width = Book.MAX_TITLE_LENGTH
        author_width = Book.MAX_AUTHOR_LENGTH
        year_width = 10
        status_width = max(len(status.value) for status in BookStatus)

        print(f'{"ID":<{id_width}} {"Название":<{title_width}} {"Автор":<{author_width}} {"Год":<{year_width}}'
              f' {"Статус":<{status_width}}')
        print('-' * (id_width + title_width + author_width + year_width + status_width))

        for book in books:
            print(f'{book.id:<{id_width}} {book.title:<{title_width}} {book.author:<{author_width}}'
                  f' {book.year:<{year_width}} {book.status.value:<{status_width}}')

    def change_status(self, book_id: int, new_status: BookStatus) -> None:
        """
        Изменяет статус книги.

        Ищет книгу по ID и изменяет ее статус на новый.

        Args:
            book_id (int): ID книги для изменения статуса.
            new_status (BookStatus): Новый статус книги.
        """

        book = self._find_book_by_id(book_id)
        if book:
            book.status = new_status
            self._save_books()
            print(f'Статус книги с ID {book_id} изменен на \'{new_status.value}\'')
        else:
            print(f'Книга с ID {book_id} не найдена')

    def exit(self):
        """
        Метод для выхода из библиотеки с сохранением изменений.
        """

        self._save_books()
