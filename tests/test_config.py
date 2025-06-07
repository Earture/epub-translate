import shutil
from pathlib import Path

from epub_translate.cli import configure
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


def test_set_config(monkeypatch):
    temp_config = Path(__file__).parent / "temp_config"
    temp_config.mkdir(exist_ok=True)
    shutil.copy(Path(__file__).parent / ".epub_translate_config", temp_config)

    monkeypatch.setattr(
        "pathlib.Path.home", lambda: Path(__file__).parent / "temp_config"
    )

    configure(api_key="set_test_api_key", model="set_test_model")

    config = get_config()

    assert config.api_key == "set_test_api_key"
    assert config.model == "set_test_model"
    with open(temp_config / ".epub_translate_config", "r") as f:
        content = f.read()
        assert "[OpenAI]" in content
        assert "api_key = set_test_api_key" in content
        assert "model = set_test_model" in content

    # sourcery skip: no-loop-in-tests
    for file in temp_config.iterdir():
        file.unlink()
    temp_config.rmdir()


def test_set_config_no_file(monkeypatch):
    temp_config = Path(__file__).parent / "temp_config"
    temp_config.mkdir(exist_ok=True)
    monkeypatch.setattr(
        "pathlib.Path.home", lambda: Path(__file__).parent / "temp_config"
    )

    configure(api_key="new_test_api_key", model="new_test_model")

    config = get_config()

    assert config.api_key == "new_test_api_key"
    assert config.model == "new_test_model"
    with open(temp_config / ".epub_translate_config", "r") as f:
        content = f.read()
        assert "[OpenAI]" in content
        assert "api_key = new_test_api_key" in content
        assert "model = new_test_model" in content

    # sourcery skip: no-loop-in-tests
    for file in temp_config.iterdir():
        file.unlink()
    temp_config.rmdir()
