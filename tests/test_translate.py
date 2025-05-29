import pytest

from epub_translate import translate

from .utils import assert_book, create_test_book


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
                "title": "Tłumaczenie",
                "file_name": "translation.xhtml",
                "language": "pl",
                "content": '<p style="font-style: italic; font-size: 0.9em;">Ta książka została przetłumaczona przy pomocy <strong>epub-translate</strong> — prostej narzędzia CLI, które wykorzystuje ChatGPT do przekładu .epub plików na dowolny język.<br/>Możesz go znaleźć na <a href="https://github.com/SpaceShaman/epub-translate" target="_blank">GitHub</a>. Jeśli tłumaczenie spełnia Twoje oczekiwania — zostaw gwiazdkę ⭐!</p>',
            },
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
