"""Сервисные функции."""
from domain.book.model import Book


def generate_path_to_store_book_file(model: Book) -> str:
    """Генерирует путь хранения файла книги."""
    return f"{model.author}/{model.name}/{model.file_name}"
