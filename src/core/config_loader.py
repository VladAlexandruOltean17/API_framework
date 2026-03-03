import configparser
import os
from pathlib import Path


def load_config(pytest_config=None):
    """
    Citeste config/config.ini si intoarce un dict cu:
    -base_url
    -timeout
    -log_level
    """
    env = (
        pytest_config.getoption("--env")
        if pytest_config and pytest_config.getoption("--env")
        else os.getenv("TEST_ENV", "DEV")
    ).upper()

    project_root = Path(__file__).resolve().parents[2]
    config_path = project_root / "config" / "config.ini" # needs this because the config.ini was not in src but at the
    # project root level

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    parser = configparser.ConfigParser()
    parser.read(config_path, encoding="utf-8")

    if env not in parser:
        raise KeyError(
            f"Environment '{env}' not found in config.ini. "
            f"Available: {parser.sections()}"
        )

    section = parser[env]

    return {
        "env": env,
        "base_url": section["base_url"],
        "timeout": parser["DEFAULT"].getint("timeout", fallback=10),
        "log_level": parser["DEFAULT"].get("log_level", fallback="DEBUG"),
    }
