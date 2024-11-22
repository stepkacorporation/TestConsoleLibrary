from functools import wraps
from typing import Iterable, Callable


def handle_input_errors(func: Callable) -> Callable:
    """
    Декоратор для обработки ошибок ввода.

    Этот декоратор повторяет выполнение обернутой функции до тех пор,
    пока она не завершится без исключений.

    Args:
        func (Callable): Функция, к которой применяется декоратор.

    Returns:
        Callable: Обернутая функция.
    """

    @wraps(func)
    def _wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f'Ошибка: {e}. Попробуйте снова')

    return _wrapper


@handle_input_errors
def get_int_input(prompt: str, valid_values: Iterable[int] | None = None) -> int:
    """
    Функция для получения числового ввода от пользователя.

    Эта функция запрашивает ввод, преобразует его в целое число и проверяет
    его на соответствие допустимым значениям.

    Args:
        prompt (str): Сообщение, отображаемое пользователю для ввода.
        valid_values (Iterable[int], optional): Набор допустимых значений.
            Если указан, введенное значение должно быть в этом наборе.

    Raises:
        ValueError: Если введенное значение не является числом или
            не входит в набор допустимых значений.

    Returns:
        int: Корректное целое число, введенное пользователем.
    """

    user_input = input(prompt).strip()

    try:
        value = int(user_input)
    except ValueError:
        raise ValueError('Введено не число')

    if valid_values and value not in valid_values:
        raise ValueError(f'Допустимые значения: {tuple(valid_values)}')

    return value


@handle_input_errors
def get_str_input(prompt: str, valid_values: Iterable[str] | None = None) -> str:
    """
    Функция для получения строкового ввода от пользователя.

    Эта функция запрашивает ввод, проверяет его на соответствие
    допустимым значениям, если они указаны.

    Args:
        prompt (str): Сообщение, отображаемое пользователю для ввода.
        valid_values (Iterable[str], optional): Набор допустимых строк.
            Если указан, введенное значение должно быть в этом наборе.

    Raises:
        ValueError: Если введенное значение не входит в набор допустимых значений.

    Returns:
        str: Корректная строка, введенная пользователем.
    """

    user_input = input(prompt).strip()

    if valid_values and user_input not in valid_values:
        raise ValueError(f'Допустимые значения: {tuple(valid_values)}')

    return user_input
