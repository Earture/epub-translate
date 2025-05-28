import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub
from openai import OpenAI


def translate(file_path: str, target_language: str) -> None:
    book = epub.read_epub(file_path)
    source_language = book.get_metadata("DC", "language")[0][0]
    _translate_chapters(book, source_language, target_language)
    _set_new_language(book, target_language)
    new_file_path = f"{file_path.replace('.epub', '')}_{target_language}.epub"
    epub.write_epub(new_file_path, book)


def _set_new_language(book: epub.EpubBook, target_language: str) -> None:
    for data in book.metadata.values():
        if "language" in data:
            data["language"].clear()
    book.set_language(target_language)


def _translate_chapters(
    book: epub.EpubBook, source_language: str, target_language: str
) -> None:
    chapters = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)
    for chapter in chapters:
        chapter_content = _get_chapter_content(chapter)
        translated_content = _translate_text(
            chapter_content,
            source_language,
            target_language,
        )
        chapter.set_content(translated_content.encode())


def _get_chapter_content(chapter: epub.EpubHtml) -> str:
    soup = BeautifulSoup(chapter.content, "html.parser")
    head = soup.head
    body = soup.body
    return str(head) + str(body)


def _translate_text(text: str, source_language: str, target_language: str) -> str:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-4o",
        instructions=(
            "You are a book translator specialized in translating "
            "HTML content while preserving the structure and tags. "
            "Translate only the inner text of the HTML, keeping all tags intact. "
            "Ensure the translation is accurate and contextually appropriate."
            f"Translate from {source_language} to {target_language}."
        ),
        input=text,
        temperature=0.0,
    )
    return response.output_text
