"""Rich Module."""

__docformat__ = "numpy"

from typing import Dict, List

from infomark import ifm

# https://rich.readthedocs.io/en/stable/appendix/colors.html#appendix-colors
# https://rich.readthedocs.io/en/latest/highlighting.html#custom-highlighters

RICH_TAGS = [
    "[menu]",
    "[/menu]",
    "[cmds]",
    "[/cmds]",
    "[info]",
    "[/info]",
    "[param]",
    "[/param]",
    "[src]",
    "[/src]",
    "[help]",
    "[/help]",
]

class MenuText:
    """Generate and format menu text with rich color tags for CLI display."""

    CMD_NAME_LENGTH = 23
    CMD_DESCRIPTION_LENGTH = 65
    CMD_PROVIDERS_LENGTH = 23
    SECTION_SPACING = 4

    def __init__(self, path: str = ""):
        """Initialize the MenuText instance."""
        self.menu_text = ""
        self.menu_path = path
        self.warnings: List[Dict[str, str]] = []

    @staticmethod
    def _get_providers(command_path: str) -> List[str]:
        """Fetch the preferred providers for the specified command.

        Parameters
        ----------
        command_path : str
            The command path to find providers for, e.g., "/equity/price/historical".

        Returns
        -------
        List[str]
            A list of providers for the specified command.
        """
        command_reference = ifm.reference.get("paths", {}).get(command_path, {})  # type: ignore
        if command_reference:
            providers = list(command_reference.get("parameters", {}).keys())
            return [provider for provider in providers if provider != "standard"]
        return []

    def _format_cmd_name(self, name: str) -> str:
        """Ensure command name fits within the maximum length."""
        if len(name) > self.CMD_NAME_LENGTH:
            truncated_name = name[:self.CMD_NAME_LENGTH]

            if "_" in name:
                name_parts = name.split("_")
                truncated_name = "_".join(name_parts[:2]) if len(name_parts) > 2 else name_parts[0]
                if len(truncated_name) > self.CMD_NAME_LENGTH:
                    truncated_name = truncated_name[:self.CMD_NAME_LENGTH]

            if truncated_name != name:
                self.warnings.append({
                    "warning": "Command name too long",
                    "actual command": f"`{name}`",
                    "displayed command": f"`{truncated_name}`",
                })
                name = truncated_name

        return name

    def _format_cmd_description(
        self, name: str, description: str, trim: bool = True
    ) -> str:
        """Ensure command description fits within the maximum length."""
        if not description or description == f"{self.menu_path}{name}":
            description = ""
        return (
            description[:self.CMD_DESCRIPTION_LENGTH - 3] + "..."
            if len(description) > self.CMD_DESCRIPTION_LENGTH and trim
            else description
        )

    def add_raw(self, text: str, left_spacing: bool = False):
        """Append unformatted text."""
        if left_spacing:
            self.menu_text += f"{self.SECTION_SPACING * ' '}{text}\n"
        else:
            self.menu_text += text

    def add_info(self, text: str):
        """Append informational text with [info] tag."""
        self.menu_text += f"[info]{text}:[/info]\n"

    def add_cmd(self, name: str, description: str = "", disable: bool = False):
        """Append command text with [cmds] tag and providers if any."""
        formatted_name = self._format_cmd_name(name)
        name_padding = (self.CMD_NAME_LENGTH - len(formatted_name)) * " "
        providers = self._get_providers(f"{self.menu_path}{name}")
        formatted_description = self._format_cmd_description(
            formatted_name,
            description,
            bool(providers),
        )
        description_padding = (
            self.CMD_DESCRIPTION_LENGTH - len(formatted_description)
        ) * " "
        spacing = self.SECTION_SPACING * " "
        cmd = f"{spacing}{formatted_name + name_padding}{spacing}{formatted_description + description_padding}"
        cmd = f"[unvl]{cmd}[/unvl]" if disable else f"[cmds]{cmd}[/cmds]"

        if providers:
            cmd += f"{spacing}[src][{', '.join(providers)}][/src]"

        self.menu_text += cmd + "\n"

    def add_menu(
        self,
        name: str,
        description: str = "",
        disable: bool = False,
    ):
        """Append menu text with [menu] tag."""
        spacing = (self.CMD_NAME_LENGTH - len(name) + self.SECTION_SPACING) * " "

        if not description or description == f"{self.menu_path}{name}":
            description = ""

        if len(description) > self.CMD_DESCRIPTION_LENGTH:
            description = description[:self.CMD_DESCRIPTION_LENGTH - 3] + "..."

        menu = f"{name}{spacing}{description}"
        tag = "unvl" if disable else "menu"
        self.menu_text += f"[{tag}]>   {menu}[/{tag}]\n"

    def add_setting(self, name: str, status: bool = True, description: str = ""):
        """Append setting text with color based on status."""
        spacing = (self.CMD_NAME_LENGTH - len(name) + self.SECTION_SPACING) * " "
        indentation = self.SECTION_SPACING * " "
        color = "green" if status else "red"

        self.menu_text += (
            f"[{color}]{indentation}{name}{spacing}{description}[/{color}]\n"
        )
