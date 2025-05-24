import os

import pytest
from ebooklib import epub

from epub_translate import translate


def create_book():
    book = epub.EpubBook()
    book.set_identifier("id123456")
    book.set_title("Test Book")
    book.set_language("en")
    epub.write_epub("test_book.epub", book)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    create_book()
    yield
    if os.path.exists("test_book.epub"):
        os.remove("test_book.epub")
    if os.path.exists("test_book_pl.epub"):
        os.remove("test_book_pl.epub")


def test_translate_epub_from_en_to_pl():
    translate("test_book.epub", "pl")

    assert os.path.exists("test_book_pl.epub")
