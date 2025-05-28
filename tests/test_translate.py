import os
from unittest import mock

import pytest

from epub_translate import translate

from .utils import assert_book, create_test_book

MOCK_TRANSLATOR = True  # Mock translator to avoid actual API calls in tests


@pytest.fixture(autouse=True)
def mock_translator():
    if MOCK_TRANSLATOR:
        with mock.patch("epub_translate.main._translate_text") as mock_translate:
            mock_translate.side_effect = lambda text, source, target: (
                text.replace(
                    "A test chapter not telling about anything.",
                    "Rozdział testowy, który nie opowiada o niczym.",
                ).replace(
                    "Another test chapter to translate.",
                    "Kolejny rozdział testowy do przetłumaczenia.",
                )
            )
            yield
    else:
        yield


@pytest.fixture(autouse=True)
def teardown():
    yield
    if os.path.exists("test_book.epub"):
        os.remove("test_book.epub")
    if os.path.exists("test_book_pl.epub"):
        os.remove("test_book_pl.epub")


def test_translate_epub_from_en_to_pl():
    create_test_book(
        language="en",
        chapters=[
            {
                "title": "Chapter 1",
                "file_name": "chapter_1.xhtml",
                "language": "en",
                "content": "<p>A test chapter not telling about anything.</p>",
            },
            {
                "title": "Chapter 2",
                "file_name": "chapter_2.xhtml",
                "language": "en",
                "content": "<p>Another test chapter to translate.</p>",
            },
        ],
    )

    translate("test_book.epub", "pl")

    assert_book(
        "test_book_pl.epub",
        language="pl",
        chapters=[
            {
                "title": "Chapter 1",
                "file_name": "chapter_1.xhtml",
                "language": "pl",
                "content": "<p>Rozdział testowy, który nie opowiada o niczym.</p>",
            },
            {
                "title": "Chapter 2",
                "file_name": "chapter_2.xhtml",
                "language": "pl",
                "content": "<p>Kolejny rozdział testowy do przetłumaczenia.</p>",
            },
        ],
    )


def test_translate_epub_from_en_to_pl_with_non_existent_file():
    with pytest.raises(FileNotFoundError):
        translate("non_existent_book.epub", "pl")
