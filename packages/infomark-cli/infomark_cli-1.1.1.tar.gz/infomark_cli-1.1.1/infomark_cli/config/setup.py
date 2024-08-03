"""Configuration setup for the CLI application."""

from pathlib import Path

from infomark_cli.config.constants import ENV_FILE_SETTINGS, SETTINGS_DIRECTORY


def initialize():
    """Prepare configurations before launching the CLI."""
    SETTINGS_DIRECTORY.mkdir(parents=True, exist_ok=True)
    Path(ENV_FILE_SETTINGS).touch(exist_ok=True)
