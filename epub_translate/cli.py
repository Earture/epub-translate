from typer import Argument, Typer
from typing_extensions import Annotated

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
