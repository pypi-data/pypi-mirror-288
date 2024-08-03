"""Settings Controller Module."""

import argparse
from functools import partial, update_wrapper
from types import MethodType
from typing import List, Literal, Optional, get_origin

from infomark_cli.config.menu_text import MenuText
from infomark_cli.controllers.base_controller import BaseController
from infomark_cli.models.settings import SettingGroups
from infomark_cli.session import Session

session = Session()


class SettingsController(BaseController):
    """Settings Controller class."""

    _COMMANDS = {
        v.json_schema_extra.get("command"): {
            "command": (v.json_schema_extra or {}).get("command"),
            "group": (v.json_schema_extra or {}).get("group"),
            "description": v.description,
            "annotation": v.annotation,
            "field_name": k,
        }
        for k, v in sorted(
            session.settings.model_fields.items(),
            key=lambda item: (item[1].json_schema_extra or {}).get("command", ""),
        )
        if v.json_schema_extra
    }
    CHOICES_COMMANDS: List[str] = list(_COMMANDS.keys())
    PATH = "/settings/"
    CHOICES_GENERATION = True

    def __init__(self, queue: Optional[List[str]] = None):
        """Initialize the Constructor."""
        super().__init__(queue)
        for cmd, field in self._COMMANDS.items():
            group = field.get("group")
            if group == SettingGroups.feature_flags:
                self._generate_command(cmd, field, "toggle")
            elif group == SettingGroups.preferences:
                self._generate_command(cmd, field, "set")
        self.update_comp
