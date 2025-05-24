import os


def translate(file_path: str, target_language: str) -> None:
    _check_file_exists(file_path)
    new_file_path = f"{file_path.replace('.epub', '')}_{target_language}.epub"
    with open(new_file_path, "w") as f:
        f.write(f"Translated {file_path} to {target_language}")


def _check_file_exists(file_path: str) -> None:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
