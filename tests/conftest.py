import os
from unittest import mock

import pytest

MOCK_TRANSLATOR = True  # Mock translator to avoid actual API calls in tests
TRANSLATION = [
    (
        "<p>A test chapter not telling about anything.</p>",
        "<p>Rozdział testowy, który nie opowiada o niczym.</p>",
    ),
    (
        "<p>Another test chapter to translate.</p>",
        "```html\n<p>Kolejny rozdział testowy do przetłumaczenia.</p>```",
    ),
    ("Chapter 1", "Rozdział 1"),
    ("Chapter 2", "Rozdział 2"),
    (
        "This book was translated using <strong>epub-translate</strong> — a simple CLI tool that leverages ChatGPT to translate .epub books into any language.",
        "Ta książka została przetłumaczona przy pomocy <strong>epub-translate</strong> — prostej narzędzia CLI, które wykorzystuje ChatGPT do przekładu .epub plików na dowolny język.",
    ),
    (
        "You can find it on",
        "Możesz go znaleźć na",
    ),
    (
        "If the translation meets your expectations — leave a star",
        "Jeśli tłumaczenie spełnia Twoje oczekiwania — zostaw gwiazdkę",
    ),
]


@pytest.fixture(autouse=True)
def teardown():
    yield
    if os.path.exists("test_book.epub"):
        os.remove("test_book.epub")
    if os.path.exists("test_book_pl.epub"):
        os.remove("test_book_pl.epub")


@pytest.fixture(autouse=True)
def mock_translator():
    if MOCK_TRANSLATOR:
        with mock.patch("epub_translate.translator.OpenAI") as mock_openai_cls:
            mock_client = mock.Mock()

            def create_side_effect(**kwargs):
                text = kwargs.get("input", "")
                for original, translated in TRANSLATION:
                    if original in text:
                        text = text.replace(original, translated)
                mock_response = mock.Mock()
                mock_response.output_text = text
                return mock_response

            mock_client.responses.create.side_effect = create_side_effect
            mock_openai_cls.return_value = mock_client
            yield
    else:
        yield
