import os

# Список расширений файлов, относящихся к проекту (Python, HTML, CSS, JS и т.д.)
PROJECT_EXTENSIONS = {'.py', '.html', '.css', '.js', '.md', '.json', '.toml', '.yml', '.json'}
# Список директорий, которые нужно игнорировать
IGNORED_DIRECTORIES = {'__pycache__', '.git', '.idea', 'node_modules', 'env', 'venv', '.venv', '__legacy', 'staticfiles'}


def print_directory_structure(root_dir, indent=""):
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)

        # Игнорируем директории, которые не относятся к проекту
        if os.path.isdir(item_path) and item in IGNORED_DIRECTORIES:
            continue

        # Игнорируем файлы, не относящиеся к проекту
        if os.path.isfile(item_path):
            _, ext = os.path.splitext(item)
            if ext not in PROJECT_EXTENSIONS:
                continue

        # Выводим название элемента с отступом
        print(indent + "|-- " + item)

        # Рекурсивно обходим поддиректории, если они не в списке игнорируемых
        if os.path.isdir(item_path) and item not in IGNORED_DIRECTORIES:
            print_directory_structure(item_path, indent + "    ")


if __name__ == "__main__":
    # Указываем текущую директорию
    current_directory = os.getcwd()
    print("Directory structure of:", current_directory)
    print_directory_structure(current_directory)
