from typer import Argument, Typer
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


@app.command(name="config")
def configure(
    api_key: Annotated[
        str | None,
        Argument(
            help="OpenAI API key to use for translation. If not provided, the default config will be used.",
            default=None,
        ),
    ] = None,
    model: Annotated[
        str | None,
        Argument(
            help="OpenAI model to use for translation. Default is 'gpt-4o'.",
            default=None,
        ),
    ] = None,
) -> None:
    set_config(api_key, model)
