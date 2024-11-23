# Система управления библиотекой (Тестовое задание)

Консольное приложение для управления библиотекой книг. Приложение позволяет добавлять, удалять, искать, отображать книги, а также изменять их статус (в наличии или выдана). Данные хранятся в JSON формате.

## Функциональные возможности

1. **Добавление книги**:
    - Пользователь вводит название книги, автора и год издания.
    - Каждая книга добавляется с уникальным идентификатором и статусом "в наличии".
  
2. **Удаление книги**:
    - Пользователь может удалить книгу по её уникальному идентификатору (ID).
  
3. **Поиск книги**:
    - Возможность поиска книг по названию, автору или году издания.
  
4. **Отображение всех книг**:
    - Выводится список всех книг с их ID, названием, автором, годом издания и статусом.
  
5. **Изменение статуса книги**:
    - Пользователь может изменить статус книги на "в наличии" или "выдана".

## Запуск

1. **Клонирование репозитория**:
    ```bash
    git clone https://github.com/stepkacorporation/TestConsoleLibrary.git
    cd TestConsoleLibrary
    ```

2. **Запуск приложения**:
    ```bash
    python -m app.main
    ```

## Тестирование

Проект включает в себя модульные тесты, которые проверяют корректность работы основных функций.

1. Для запуска тестов выполните:
    ```bash
    python -m unittest discover -s tests
    ```

2. Если требуется запустить тесты для определённого модуля, выполните:
    ```bash
    python -m unittest tests.library.test_library
    ```
   
Приятного использования! 😊