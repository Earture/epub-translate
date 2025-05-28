from ebooklib import ITEM_DOCUMENT, epub
from openai import OpenAI


def translate(file_path: str, target_language: str) -> None:
    book = epub.read_epub(file_path)
    source_language = book.get_metadata("DC", "language")[0][0]
    _translate_items(book, source_language, target_language)
    _set_new_language(book, target_language)
    new_file_path = f"{file_path.replace('.epub', '')}_{target_language}.epub"
    epub.write_epub(new_file_path, book)


def _set_new_language(book: epub.EpubBook, target_language: str) -> None:
    for data in book.metadata.values():
        if "language" in data:
            data["language"].clear()
    book.set_language(target_language)


def _translate_items(
    book: epub.EpubBook, source_language: str, target_language: str
) -> None:
    chapters = book.get_items_of_type(ITEM_DOCUMENT)
    for chapter in chapters:
        chapter_content = chapter.content.decode()
        if "<body" not in chapter_content or 'type="toc"' in chapter_content:
            continue
        extracted_content = _extract_body_content(chapter_content)
        translated_content = _translate_text(
            extracted_content,
            source_language,
            target_language,
        )
        chapter.content = _replace_body_content(
            chapter_content, translated_content
        ).encode()


def _extract_body_content(text: str) -> str:
    start = text.find("<body")
    text = text[start:]
    start = text.find(">") + 1
    end = text.rfind("</body>")
    return text[start:end].strip()


def _replace_body_content(original_text: str, new_content: str) -> str:
    start = original_text.find("<body")
    end = original_text.rfind("</body>")
    return (
        original_text[: start + original_text[start:].find(">") + 1]
        + new_content
        + original_text[end:]
    )


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
    return _normalize_translation(response.output_text)


def _normalize_translation(text: str) -> str:
    return text[text.find("<") : text.rfind(">") + 1]
