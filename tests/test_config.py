from pathlib import Path

from epub_translate.config import get_config


def test_get_config(monkeypatch):
    monkeypatch.setattr("pathlib.Path.home", lambda: Path(__file__).parent)

    config = get_config()

    assert config.api_key == "test_api_key"
    assert config.model == "gpt-test"


def test_get_config_no_file(monkeypatch):
    temp_config = Path(__file__).parent / "temp_config"
    temp_config.mkdir(exist_ok=True)
    monkeypatch.setattr(
        "pathlib.Path.home", lambda: Path(__file__).parent / "temp_config"
    )

    config = get_config()

    assert config.api_key == ""
    assert config.model == "gpt-4o"

    with open(temp_config / ".epub_translate_config", "r") as f:
        content = f.read()
        assert "[OpenAI]" in content
        assert "api_key =" in content
        assert "model = gpt-4o" in content

    # sourcery skip: no-loop-in-tests
    for file in temp_config.iterdir():
        file.unlink()
    temp_config.rmdir()
