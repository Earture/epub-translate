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
        with mock.patch("epub_translate.main.OpenAI") as mock_openai_cls:
            mock_client = mock.Mock()

            def create_side_effect(**kwargs):
                text = kwargs.get("input", "")
                for original, translated in TRANSLATION:
                    if original in text:
                        output = text.replace(original, translated)
                        break
                mock_response = mock.Mock()
                mock_response.output_text = output
                return mock_response

            mock_client.responses.create.side_effect = create_side_effect
            mock_openai_cls.return_value = mock_client
            yield
    else:
        yield
