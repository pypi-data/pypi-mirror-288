""""Infomark Terminal CLI utilities."""

import json
from pathlib import Path

HOME_DIR = Path.home()
INFOMARK_DIR = Path(HOME_DIR, ".infomark")
SETTINGS_FILE_PATH = Path(INFOMARK_DIR, "system_settings.json")


def update_logging_context() -> str:
    """Update Infomark Terminal logging context in settings."""
    with open(SETTINGS_FILE_PATH) as file:
        settings = json.load(file)

    previous_logging_context = settings.get("logging_context", "")

    settings["logging_context"] = "cli"

    with open(SETTINGS_FILE_PATH, "w") as file:
        json.dump(settings, file, indent=4)

    return previous_logging_context


def restore_logging_context(previous_logging_context: str):
    """Restore the original Infomark Terminal logging context in settings."""
    with open(SETTINGS_FILE_PATH) as file:
        settings = json.load(file)

    settings["logging_context"] = previous_logging_context

    with open(SETTINGS_FILE_PATH, "w") as file:
        json.dump(settings, file, indent=4)
