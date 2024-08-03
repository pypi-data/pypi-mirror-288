""""Infomark Terminal Settings Model."""

from enum import Enum
from typing import Any, Literal

from dotenv import dotenv_values, set_key
from infomark_cli.config.constants import AVAILABLE_ICONS, ENV_FILE_SETTINGS
from infomark_core.app.version import get_package_version
from pydantic import BaseModel, ConfigDict, Field, model_validator
from pytz import all_timezones

VERSION = get_package_version("infomark-cli")


class SettingCategories(Enum):
    """Categories for settings."""

    feature_flags = "feature_flag"
    preferences = "preference"


class Settings(BaseModel):
    """Settings model for Infomark Terminal."""

    # Terminal version
    VERSION: str = VERSION

    # DEVELOPMENT FLAGS
    TEST_MODE: bool = False
    DEBUG_MODE: bool = False
    DEV_BACKEND: bool = False

    # INFOMARK
    HUB_URL: str = "https://my.infomark.co"
    BASE_URL: str = "https://payments.infomark.co"

    # GENERAL
    PREVIOUS_USE: bool = False

    # FEATURE FLAGS
    FILE_OVERWRITE: bool = Field(
        default=False,
        description="Whether to overwrite files if they already exist",
        command="overwrite",
        group=SettingCategories.feature_flags,
    )
    SHOW_VERSION: bool = Field(
        default=True,
        description="Whether to display the version in the bottom corner",
        command="version",
        group=SettingCategories.feature_flags,
    )
    USE_INTERACTIVE_DF: bool = Field(
        default=True,
        description="Display tables in an interactive window",
        command="interactive",
        group=SettingCategories.feature_flags,
    )
    USE_CLEAR_AFTER_CMD: bool = Field(
        default=False,
        description="Clear console after each command",
        command="cls",
        group=SettingCategories.feature_flags,
    )
    USE_DATETIME: bool = Field(
        default=True,
        description="Show date and time before the flair",
        command="datetime",
        group=SettingCategories.feature_flags,
    )
    USE_PROMPT_TOOLKIT: bool = Field(
        default=True,
        description="Enable prompt toolkit for autocomplete and history",
        command="promptkit",
        group=SettingCategories.feature_flags,
    )
    ENABLE_EXIT_AUTO_HELP: bool = Field(
        default=True,
        description="Automatically show help when exiting menu",
        command="exithelp",
        group=SettingCategories.feature_flags,
    )
    ENABLE_RICH_PANEL: bool = Field(
        default=True,
        description="Enable colorful rich CLI panel",
        command="richpanel",
        group=SettingCategories.feature_flags,
    )
    TOOLBAR_HINT: bool = Field(
        default=True,
        description="Display usage hints in the bottom toolbar",
        command="tbhint",
        group=SettingCategories.feature_flags,
    )
    SHOW_MSG_REGISTRY: bool = Field(
        default=False,
        description="Show registry message after adding a new result",
        command="registry_msg",
        group=SettingCategories.feature_flags,
    )

    # PREFERENCES
    TIMEZONE: Literal[tuple(all_timezones)] = Field(  # type: ignore[valid-type]
        default="America/New_York",
        description="Select timezone",
        command="timezone",
        group=SettingCategories.preferences,
    )
    ICON: Literal[tuple(AVAILABLE_ICONS)] = Field(  # type: ignore[valid-type]
        default=":infomark",
        description="Choose an icon",
        command="icon",
        group=SettingCategories.preferences,
    )
    MAX_REGISTRY_SIZE: int = Field(
        default=10,
        description="Maximum number of items in the registry",
        command="registry_size",
        group=SettingCategories.preferences,
    )
    DISPLAY_REGISTRY_SIZE: int = Field(
        default=5,
        description="Maximum number of items to display in the help menu",
        command="registry_display",
        group=SettingCategories.preferences,
    )
    STYLE: str = Field(
        default="dark",
        description="Apply a custom style to the CLI",
        command="style",
        group=SettingCategories.preferences,
    )
    MAX_ROWS: int = Field(
        default=20,
        description="Number of rows to display (when not using interactive tables)",
        command="max_rows",
        group=SettingCategories.preferences,
    )
    MAX_COLUMNS: int = Field(
        default=5,
        description="Number of columns to display (when not using interactive tables)",
        command="max_columns",
        group=SettingCategories.preferences,
    )

    model_config = ConfigDict(validate_assignment=True)

    def __repr__(self) -> str:
        """Return a string representation of the settings."""
        return f"{self.__class__.__name__}\n\n" + "\n".join(
            f"{k}: {v}" for k, v in self.model_dump().items()
        )

    @model_validator(mode="before")
    @classmethod
    def from_env(cls, values: dict) -> dict:
        """Load settings from .env file."""
        settings = {}
        settings.update(dotenv_values(ENV_FILE_SETTINGS))
        settings.update(values)
        filtered = {k.replace("INFOMARK_", ""): v for k, v in settings.items()}
        return filtered

    def set_item(self, key: str, value: Any) -> None:
        """Set an item in the model and update the .env file."""
        setattr(self, key, value)
        set_key(str(ENV_FILE_SETTINGS), "INFOMARK_" + key, str(value))
