"""Utilities for handling chart styles in Infomark."""

# pylint: disable=C0302,R0902,W3301
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from rich.console import Console

from infomark_cli.config.constants import STYLES_DIRECTORY

console = Console()


class Style:
    """A class for managing style configurations in Infomark.

    This class supports style management for two libraries: Plotly and Rich.
    It provides absolute paths to `.pltstyle` files for Plotly and Python dictionaries
    for Rich's custom styles.
    """

    STYLES_REPO = STYLES_DIRECTORY

    console_styles_available: Dict[str, Path] = {}
    console_style: Dict[str, Any] = {}

    line_color: str = ""
    up_color: str = ""
    down_color: str = ""
    up_colorway: List[str] = []
    down_colorway: List[str] = []
    up_color_transparent: str = ""
    down_color_transparent: str = ""

    line_width: float = 1.5

    def __init__(
        self,
        style: Optional[str] = "",
        directory: Optional[Path] = None,
    ):
        """Initialize the Style class."""
        self._load(directory)
        self.apply(style, directory)

    def apply(
        self, style: Optional[str] = None, directory: Optional[Path] = None
    ) -> None:
        """Apply a specified style to the console."""
        if style:
            if style in self.console_styles_available:
                json_path: Optional[Path] = self.console_styles_available[style]
            else:
                self._load(directory)
                if style in self.console_styles_available:
                    json_path = self.console_styles_available[style]
                else:
                    console.print(f"\nStyle '{style}' not found, reverting to default.")
                    json_path = self.console_styles_available.get("dark", None)

            if json_path:
                self.console_style = self._load_from_json(json_path)
            else:
                console.print("Failed to load the default style.")

    def _from_directory(self, folder: Optional[Path]) -> None:
        """Load custom styles from the specified directory.

        This method looks into default and user folders, loading styles
        based on naming conventions:
        *.pltstyle        - for Plotly stylesheets
        *.richstyle.json  - for Rich stylesheets

        Parameters
        ----------
        folder : Path
            The path to the directory containing the style files.
        """
        if not folder or not folder.exists():
            return

        for attr, ext in zip(
            ["console_styles_available"],
            [".richstyle.json"],
        ):
            for file in folder.rglob(f"*{ext}"):
                getattr(self, attr)[file.name.replace(ext, "")] = file

    def _load(self, directory: Optional[Path] = None) -> None:
        """Load style files from both default and user directories."""
        self._from_directory(self.STYLES_REPO)
        self._from_directory(directory)

    def _load_from_json(self, file: Path) -> Dict[str, Any]:
        """Load style configuration from a JSON file."""
        with open(file) as f:
            json_style: dict = json.load(f)
            for key, value in json_style.items():
                json_style[key] = value.replace(
                    " ", ""
                )  # Remove spaces to ensure compatibility with Rich
            return json_style

    @property
    def available_styles(self) -> List[str]:
        """Get a list of available console styles."""
        return list(self.console_styles_available.keys())
