import os

from ebooklib import epub


def translate(file_path: str, target_language: str) -> None:
    _check_file_exists(file_path)
    book = epub.read_epub(file_path)
    _set_new_language(book, target_language)
    new_file_path = f"{file_path.replace('.epub', '')}_{target_language}.epub"
    epub.write_epub(new_file_path, book)


def _set_new_language(book: epub.EpubBook, target_language: str) -> None:
    for data in book.metadata.values():
        if "language" in data:
            data["language"].clear()
    book.set_language(target_language)


def _check_file_exists(file_path: str) -> None:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
