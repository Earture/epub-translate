from ebooklib import ITEM_DOCUMENT, epub
from openai import OpenAI
from tqdm import tqdm

from .config import get_config


def translate_epub(file_path: str, target_language: str) -> None:
    book = epub.read_epub(file_path)
    source_language = book.get_metadata("DC", "language")[0][0]
    _translate_chapters(book, source_language, target_language)
    _set_new_language(book, target_language)
    _add_translation_chapter(book, source_language, target_language)
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
    chapters = book.get_items_of_type(ITEM_DOCUMENT)
    for chapter in tqdm(chapters, total=len(book.toc), desc="Translating chapters"):
        if _is_not_chapter(chapter):
            continue
        _translate_chapter(chapter, source_language, target_language)


def _is_not_chapter(chapter: epub.EpubHtml) -> bool:
    chapter_content = chapter.content.decode()
    return "<body" not in chapter_content or 'type="toc"' in chapter_content


def _translate_chapter(
    chapter: epub.EpubHtml, source_language: str, target_language: str
) -> None:
    chapter_content = chapter.content.decode()
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
    config = get_config()
    client = OpenAI(api_key=config.api_key)
    response = client.responses.create(
        model=config.model,
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


def _add_translation_chapter(
    book: epub.EpubBook, source_language: str, target_language: str
) -> None:
    content = (
        "<p style='font-style: italic; font-size: 0.9em;'>"
        "This book was translated using <strong>epub-translate</strong> — a simple CLI tool that leverages ChatGPT to translate .epub books into any language."
        "<br>"
        "You can find it on <a href='https://github.com/SpaceShaman/epub-translate' target='_blank'>GitHub</a>. If the translation meets your expectations — leave a star ⭐!</p>"
    )
    content = _translate_text(content, source_language, target_language)
    translation_chapter = epub.EpubHtml(
        title="Translation",
        file_name="translation.xhtml",
        lang=target_language,
        uid="translation",
    )
    translation_chapter.set_content(content)
    book.add_item(translation_chapter)
    book.toc.insert(0, translation_chapter)
    book.spine.insert(0, translation_chapter)
