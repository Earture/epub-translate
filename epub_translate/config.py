from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    api_key: str = ""
    api_base: str = ""
    model: str = "gpt-4o"


def get_config() -> Config:
    config_path = Path.home() / ".epub_translate_config"
    config = ConfigParser()
    if config_path.exists():
        config.read(config_path)
    else:
        config["OpenAI"] = {"api_key": "","api_base": "", "model": "gpt-4o"}
        with config_path.open("w") as config_file:
            config.write(config_file)
    return Config(
        api_key=config.get("OpenAI", "api_key", fallback=""),
        model=config.get("OpenAI", "model", fallback="gpt-4o"),
        api_base=config.get("OpenAI", "api_base", fallback="http://127.0.0.1:1234/v1")
    )


def set_config(api_key: str | None = None,api_base: str | None = None, model: str | None = None) -> None:
    config_path = Path.home() / ".epub_translate_config"
    config = ConfigParser()
    if config_path.exists():
        config.read(config_path)
    else:
        config["OpenAI"] = {"api_key": "","api_base": "", "model": "gpt-4o"}

    if api_key is not None:
        config["OpenAI"]["api_key"] = api_key
    if api_base is not None:
        config["OpenAI"]["api_base"] = api_base
    if model is not None:
        config["OpenAI"]["model"] = model

    with config_path.open("w") as config_file:
        config.write(config_file)
