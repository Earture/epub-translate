from typer import Argument, Option, Typer
from typing_extensions import Annotated

from .config import set_config
from .translator import translate_epub

app = Typer()


@app.command()
def translate(
    file_path: Annotated[
        str, Argument(help="Path to the EPUB file to translate, e.g., 'book.epub'.")
    ],
    target_language: Annotated[
        str,
        Argument(help="Target language code for translation, e.g., 'pl' for Polish."),
    ],
) -> None:
    translate_epub(file_path, target_language)


@app.command()
def configure(
    api_key: Annotated[
        str | None,
        Option(
            help="OpenAI API key to use for translation. If not provided, the default config will be used.",
            show_default=False,
        ),
    ] = None,
    model: Annotated[
        str | None,
        Option(
            help="OpenAI model to use for translation. Default is 'gpt-4o'.",
            show_default=False,
        ),
    ] = None,
) -> None:
    set_config(api_key, model)
