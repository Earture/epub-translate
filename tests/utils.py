from typing import TypedDict

from ebooklib import epub


class Chapter(TypedDict):
    title: str
    file_name: str
    language: str
    content: str


def create_test_book(language: str, chapters: list[Chapter]) -> None:
    book = epub.EpubBook()
    book.set_identifier("test_book")
    book.set_title("Test Book")
    book.set_language(language)
    book.add_author("Author Name")
    book.toc = []
    book.spine = ["nav"]
    for chapter in chapters:
        chapter_item = epub.EpubHtml(
            title=chapter["title"],
            file_name=chapter["file_name"],
            lang=chapter["language"],
        )
        chapter_item.set_content(chapter["content"])
        book.add_item(chapter_item)
        book.toc.append(chapter_item)
        book.spine.append(chapter_item)  # type: ignore
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    epub.write_epub("test_book.epub", book)


def assert_book(path: str, language: str, chapters: list[Chapter]) -> None:
    book = epub.read_epub(path)
    assert book.get_metadata("DC", "language") == [(language, {})]
    for chapter in chapters:
        chapter_item = book.get_item_with_href(chapter["file_name"])
        assert chapter_item is not None
        chapter_content = chapter_item.content.decode()
        assert chapter["content"] in chapter_content
        assert (
            f'lang="{chapter["language"]}" xml:lang="{chapter["language"]}"'
            in chapter_content
        )
