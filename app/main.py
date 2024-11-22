from app.library import Library, BookInterface, BookStatus
from app.utils import get_int_input, get_str_input


def main(library_: Library):
    """Основная функция для взаимодействия с пользователем."""

    while True:
        print(
            '\n1. Добавить книгу\n'
            '2. Удалить книгу\n'
            '3. Найти книгу\n'
            '4. Показать все книги\n'
            '5. Изменить статус книги\n'
            '6. Выйти\n'
        )

        choice = get_int_input('Выберите действие: ', valid_values=range(1, 7))

        if choice == 1:
            # Добавляем книгу
            title = BookInterface.input_title()
            author = BookInterface.input_author()
            year = BookInterface.input_year()
            print()
            library_.add_book(title, author, year)
            print(f'{"-" * 25}')

        elif choice == 2:
            # Удаляем книгу
            book_id = BookInterface.input_id('Введите ID книги для удаления: ')
            print()
            library_.delete_book(book_id)
            print(f'{"-" * 25}')

        elif choice == 3:
            # Ищем книгу
            field = get_str_input(
                f'Введите по какому полю искать {library_.SEARCH_FIELDS}: ',
                valid_values=library_.SEARCH_FIELDS
            )
            keyword = get_str_input('Введите ключевое слово для поиска: ')
            print()
            found_books = library_.search_books(keyword, field)
            if found_books:
                print('Результат поиска:')
                library_.display_books(found_books)
            else:
                print('Книги не найдены.')
            print(f'{"-" * 25}')

        elif choice == 4:
            # Выводим список доступных книг
            print()
            library_.list_books()
            print(f'{"-" * 25}')

        elif choice == 5:
            # Изменяем статус книги
            book_id = BookInterface.input_id('Введите ID книги для изменения статуса: ')
            new_status: BookStatus = BookInterface.input_status(f'Введите новый статус {tuple(BookStatus.values())}: ')
            print()
            library_.change_status(book_id, new_status)
            print(f'{"-" * 25}')

        elif choice == 6:
            # Завершаем работу
            library_.exit()
            print('\nСпасибо за использование библиотеки!')
            break

        else:
            print(f'Неверный выбор. Попробуйте снова')


if __name__ == '__main__':
    library = Library()
    try:
        main(library)
    except KeyboardInterrupt:
        library.exit()
        print('\n\nСпасибо за использование библиотеки!')
