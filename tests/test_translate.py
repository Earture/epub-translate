import os

import pytest
from ebooklib import epub

from epub_translate import translate


def create_book():
    book = epub.EpubBook()
    book.set_identifier("id123456")
    book.set_title("Test Book")
    book.set_language("en")
    book.add_author("Author Name")
    chapter_1 = epub.EpubHtml(title="Chapter 1", file_name="chapter1.xhtml", lang="en")
    chapter_1.content = "<h1>Chapter 1</h1><p>This is the first chapter.</p>"
    book.add_item(chapter_1)
    book.toc = (
        epub.Link("chapter1.xhtml", "Chapter 1", "chapter1"),
        (epub.Section("Introduction"), (chapter_1,)),
    )
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["nav", chapter_1]
    epub.write_epub("test_book.epub", book)


@pytest.fixture(autouse=True)
def teardown():
    yield
    if os.path.exists("test_book.epub"):
        os.remove("test_book.epub")
    if os.path.exists("test_book_pl.epub"):
        os.remove("test_book_pl.epub")


def test_translate_epub_from_en_to_pl():
    create_book()

    translate("test_book.epub", "pl")

    assert os.path.exists("test_book_pl.epub")
    translated_book = epub.read_epub("test_book_pl.epub")
    assert translated_book.get_metadata("DC", "language") == [("pl", {})]


def test_translate_epub_from_en_to_pl_with_non_existent_file():
    with pytest.raises(FileNotFoundError):
        translate("non_existent_book.epub", "pl")
