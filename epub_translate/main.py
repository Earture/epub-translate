def translate(file_path: str, target_language: str) -> None:
    new_file_path = f"{file_path.replace('.epub', '')}_{target_language}.epub"
    with open(new_file_path, "w") as f:
        f.write(f"Translated {file_path} to {target_language}")
