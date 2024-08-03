""""Configuration module."""

import sys
from pathlib import Path
from typing import Optional

from infomark import core
from infomark_core.app.model.abstract.singleton import SingletonMeta
from infomark_core.app.model.user_settings import UserSettings as User
from prompt_toolkit import PromptSession

from infomark_cli.argparse_translator.registry import Registry
from infomark_cli.config.history import CustomFileHistory
from infomark_cli.config.console import Console
from infomark_cli.config.constants import PROMPT_HISTORY_FILE
from infomark_cli.config.style import Style
from infomark_cli.models.settings import Settings


class SessionManager(metaclass=SingletonMeta):
    """Manages session settings and resources."""

    def __init__(self):
        """Initialize the session manager."""
        self._core = core
        self._settings = Settings()
        self._style = Style(
            style=self._settings.RICH_STYLE,
            directory=Path(self._core.user.preferences.styles_directory),  # type: ignore[union-attr]
        )
        self._console = Console(
            settings=self._settings, style=self._style.console_style
        )
        self._prompt_session = self._create_prompt_session()
        self._registry = Registry()

    @property
    def user(self) -> User:
        """Retrieve the current user."""
        return self._core.user  # type: ignore[union-attr]

    @property
    def settings(self) -> Settings:
        """Retrieve the current settings."""
        return self._settings

    @property
    def style(self) -> Style:
        """Retrieve the current style settings."""
        return self._style

    @property
    def console(self) -> Console:
        """Retrieve the console instance."""
        return self._console

    @property
    def registry(self) -> Registry:
        """Retrieve the object registry."""
        return self._registry

    @property
    def prompt_session(self) -> Optional[PromptSession]:
        """Retrieve the prompt session."""
        return self._prompt_session

    def _create_prompt_session(self) -> Optional[PromptSession]:
        """Set up a prompt session if interactive."""
        try:
            if sys.stdin.isatty():
                return PromptSession(
                    history=CustomFileHistory(str(PROMPT_HISTORY_FILE))
                )
            return None
        except Exception:
            return None

    def is_local_user(self) -> bool:
        """Determine if the user is local."""
        return not bool(self.user.profile.hub_session)

    def has_exceeded_max_registry(self) -> bool:
        """Check if the maximum number of registry objects has been reached."""
        return (
            len(self.registry.all) >= self.settings.MAX_REGISTRY_SIZE
        )
