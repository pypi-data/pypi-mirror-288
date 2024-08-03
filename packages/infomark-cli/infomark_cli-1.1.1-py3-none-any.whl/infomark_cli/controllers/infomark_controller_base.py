""""Infomark Terminal Base Controller."""

import argparse
import difflib
import os
import re
import shlex
from abc import ABCMeta, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

import pandas as pd
from infomark_cli.config.completer import NestedCompleter
from infomark_cli.config.constants import SCRIPT_TAGS
from infomark_cli.controllers.choices import build_controller_choice_map
from infomark_cli.controllers.hub_service import upload_routine
from infomark_cli.controllers.utils import (
    verify_file_type,
    ensure_positive,
    extract_flair_and_user,
    handle_display,
    split_and_parse_input,
    convert_unknown_args_to_dict,
    display_guest_message,
    render_rich_table,
    delete_file,
    clear_system,
    validate_key,
)
from infomark_cli.session import Session
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style

# pylint: disable=C0301,C0302,R0902,global-statement,too-many-boolean-expressions
# pylint: disable=R0912

controllers: Dict[str, Any] = {}
session = Session()


# TODO: We should try to avoid these global variables
RECORD_SESSION = False
RECORD_LOCAL_ONLY = False
RECORDED_SESSION = list()
RECORDED_SESSION_NAME = ""
RECORDED_SESSION_DESCRIPTION = ""
RECORDED_SESSION_TAGS = ""
RECORDED_SESSION_PUBLIC = False


class BaseController(metaclass=ABCMeta):
    """Base class for a CLI controller."""

    COMMON_CHOICES = [
        "cls",
        "home",
        "h",
        "?",
        "help",
        "q",
        "quit",
        "..",
        "e",
        "exit",
        "r",
        "reset",
        "stop",
        "whoami",
        "results",
    ]

    COMMAND_CHOICES: List[str] = []
    MENU_CHOICES: List[str] = []
    NEWS_CHOICES: dict = {}
    COMMAND_DELIMITER = "/"
    KEYS_MENU_PATH = "keys" + COMMAND_DELIMITER
    PATH: str = ""
    FILE_PATH: str = ""
    CHOICES_GENERATION_ENABLED = False

    @property
    def default_choices(self):
        """Return the default choices for the controller."""
        return (
            build_controller_choice_map(controller=self)
            if self.CHOICES_GENERATION_ENABLED
            else {}
        )

    def __init__(self, job_queue: Optional[List[str]] = None) -> None:
        """Initialize the base controller.

        queue: List[str]
            The current job queue, separated by "/"
            Example: /stocks/load gme/dps/sidtc/../exit
        """
        self.validate_path()
        self.path_segments = [x for x in self.PATH.split("/") if x != ""]
        self.queue = (
            self.parse_input(input_data="/".join(job_queue))
            if (job_queue and self.PATH != "/")
            else list()
        )

        controller_choices = self.COMMAND_CHOICES + self.MENU_CHOICES
        self.controller_choices = (
            controller_choices + self.COMMON_CHOICES
            if controller_choices
            else self.COMMON_CHOICES
        )

        self.completer: Union[None, NestedCompleter] = None

        self.parser = argparse.ArgumentParser(
            add_help=False,
            prog=self.path_segments[-1] if self.PATH != "/" else "cli",
        )
        self.parser.exit_on_error = False  # type: ignore
        self.parser.add_argument("cmd", choices=self.controller_choices)

    def update_completer(self, choices) -> None:
        """Update the command completer with new choices."""
        if session.prompt_session and session.settings.USE_PROMPT_TOOLKIT:
            self.completer = NestedCompleter.from_nested_dict(choices)

    def validate_path(self) -> None:
        """Ensure the command path is valid."""
        if not self.PATH.startswith("/"):
            raise ValueError("Path must start with a '/' character.")
        if not self.PATH.endswith("/"):
            raise ValueError("Path must end with a '/' character.")
        if not re.match("^[a-z/]*$", self.PATH):
            raise ValueError("Path can only contain lowercase letters and '/'.")

    def load_instance(self, class_instance, *args, **kwargs):
        """Load an existing instance of the controller or create a new one."""
        self.store_instance()
        if class_instance.PATH in controllers and len(args) + len(kwargs) == 1:
            existing_instance = controllers[class_instance.PATH]
            existing_instance.queue = self.queue
            return existing_instance.display_menu()
        return class_instance(*args, **kwargs).display_menu()

    def store_instance(self) -> None:
        """Store the current instance of the controller for future use."""
        controllers[self.PATH] = self

    def custom_reset(self) -> List[str]:
        """Implement a custom reset.

        To be overridden by child classes with specific reset behavior.
        """
        return []

    @abstractmethod
    def print_help(self) -> None:
        """Print help information."""
        raise NotImplementedError("Must override print_help.")

    def parse_input(self, input_data: str) -> list:
        """Parse user input into a list of commands.

        Handles command chain input, splitting by forward slashes.

        Parameters
        ----------
        input_data : str
            The user input string

        Returns
        ----------
        list
            List of commands to execute
        """
        custom_filters: list = []
        commands = split_and_parse_input(
            input_data=input_data, custom_filters=custom_filters
        )
        return commands

    def dispatch(self, input_data: str) -> List[str]:
        """Process and dispatch commands based on input.

        Returns
        ----------
        List[str]
            List of commands to execute
        """
        actions = self.parse_input(input_data)

        if input_data and input_data != "reset":
            session.console.print()

        if not actions:
            pass

        elif len(actions) > 1:
            if not actions[0]:
                actions[0] = "home"
            for cmd in actions[::-1]:
                if cmd:
                    self.queue.insert(0, cmd)

        else:
            try:
                (known_args, other_args) = self.parser.parse_known_args(
                    shlex.split(input_data)
                )
            except Exception as exc:
                raise SystemExit from exc

            if RECORD_SESSION:
                RECORDED_SESSION.append(input_data)

            if known_args.cmd:
                if known_args.cmd in ("..", "q"):
                    known_args.cmd = "quit"
                elif known_args.cmd in ("e"):
                    known_args.cmd = "exit"
                elif known_args.cmd in ("?", "h"):
                    known_args.cmd = "help"
                elif known_args.cmd == "r":
                    known_args.cmd = "reset"

            getattr(
                self,
                "execute_" + known_args.cmd,
                lambda _: "Command not recognized!",
            )(other_args)

        if (
            input_data
            and input_data != "reset"
            and (
                not self.queue or (self.queue and self.queue[0] not in ("quit", "help"))
            )
        ):
            session.console.print()

        return self.queue

    def execute_cls(self, _) -> None:
        """Process the 'cls' command."""
        clear_system()
        def call_home(self, _) -> None:
        """Process home command."""
        self.save_class()
        if self.PATH.count("/") == 1 and session.settings.ENABLE_EXIT_AUTO_HELP:
            self.print_help()
        self.queue = ["quit"] * (self.PATH.count("/") - 1) + self.queue

    def call_help(self, _) -> None:
        """Process help command."""
        self.print_help()

    def call_quit(self, _) -> None:
        """Process quit command."""
        self.save_class()
        self.queue.insert(0, "quit")

    def call_exit(self, _) -> None:
        """Process exit command."""
        self.save_class()
        self.queue = ["quit"] * (self.PATH.count("/") + 1) + self.queue

        if not session.is_local():
            remove_file(Path(session.user.preferences.export_directory, "routines", "hub"))

    def call_reset(self, _) -> None:
        """Process reset command."""
        self.save_class()
        if self.PATH != "/":
            self.queue = (self.custom_reset() if self.custom_reset() else list(self.path[::-1])) + ["reset"] + ["quit"] * len(self.path)

    def call_record(self, other_args) -> None:
        """Process record command."""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="record",
            description="Start recording session into .infomark routine file"
        )
        parser.add_argument("-n", "--name", type=str, help="Routine title name", nargs="+")
        parser.add_argument("-d", "--description", type=str, help="Routine description", default=f"Routine recorded at {datetime.now().strftime('%H:%M')} from the Infomark Terminal CLI", nargs="+")
        parser.add_argument("--tag1", type=str, help=f"Routine tag. Choose from: {', '.join(SCRIPT_TAGS)}", nargs="+")
        parser.add_argument("--tag2", type=str, help=f"Routine tag. Choose from: {', '.join(SCRIPT_TAGS)}", nargs="+")
        parser.add_argument("--tag3", type=str, help=f"Routine tag. Choose from: {', '.join(SCRIPT_TAGS)}", nargs="+")
        parser.add_argument("-p", "--public", action="store_true", help="Make routine public")

        if other_args and not other_args[0].startswith("-"):
            other_args.insert(0, "-n")

        ns_parser, _ = self.parse_simple_args(parser, other_args)

        if ns_parser:
            if not ns_parser.name:
                session.console.print("[red]Set a routine title using '-n'. E.g. 'record -n Morning routine'[/red]")
                return

            for tag in [ns_parser.tag1, ns_parser.tag2, ns_parser.tag3]:
                if tag and tag not in SCRIPT_TAGS:
                    session.console.print(f"[red]Tags must be one of: {', '.join(SCRIPT_TAGS)}[/red]")
                    return

            if session.is_local():
                session.console.print("[red]Recording to Infomark Hub is not supported in guest mode.[/red]")
                session.console.print("\n[yellow]Visit http://my.infomark.co to register.[/yellow]")
                session.console.print("\n[yellow]Your routine will be saved locally.[/yellow]\n")
            
            title = " ".join(ns_parser.name) if ns_parser.name else ""
            if not re.match(r"^[a-zA-Z0-9\s]+$", title):
                session.console.print(f"[red]Title '{title}' contains invalid characters. Use only digits, letters, and spaces.[/red]")
                return

            global RECORD_SESSION, RECORD_SESSION_LOCAL_ONLY, SESSION_RECORDED_NAME, SESSION_RECORDED_DESCRIPTION, SESSION_RECORDED_TAGS, SESSION_RECORDED_PUBLIC

            RECORD_SESSION_LOCAL_ONLY = session.is_local()
            RECORD_SESSION = True
            SESSION_RECORDED_NAME = title
            SESSION_RECORDED_DESCRIPTION = " ".join(ns_parser.description) if ns_parser.description else ""
            SESSION_RECORDED_TAGS = ",".join(filter(None, [ns_parser.tag1, ns_parser.tag2, ns_parser.tag3]))
            SESSION_RECORDED_PUBLIC = ns_parser.public

            session.console.print(f"[green]Recording routine '{title}' started.[/green]")
            session.console.print("\n[yellow]Remember to run 'stop' when finished!\n[/yellow]")

    def call_stop(self, other_args) -> None:
        """Process stop command."""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="stop",
            description="Stop recording session into .infomark routine file"
        )
        _, _ = self.parse_simple_args(parser, other_args)

        if "-h" not in other_args and "--help" not in other_args:
            if not RECORD_SESSION:
                session.console.print("[red]No session is being recorded. Start one using 'record'[/red]\n")
            elif len(SESSION_RECORDED) < 5:
                session.console.print("[red]Run at least 4 commands before stopping recording.[/red]\n")
            else:
                current_user = session.user
                if RECORD_SESSION_LOCAL_ONLY:
                    title_for_local_storage = SESSION_RECORDED_NAME.replace(" ", "_") + ".infomark"
                    routine_file = os.path.join(f"{current_user.preferences.export_directory}/routines", title_for_local_storage)

                    if os.path.isfile(routine_file):
                        response = session.console.input("A local routine with the same name exists. Override? (y/n): ").lower()
                        while response not in ["y", "n"]:
                            response = session.console.input("Select 'y' or 'n': ").lower()

                        if response == "n":
                            new_name = datetime.now().strftime("%Y%m%d_%H%M%S_") + title_for_local_storage
                            routine_file = os.path.join(current_user.preferences.export_directory, "routines", new_name)
                            session.console.print(f"[yellow]Routine name updated to '{new_name}'[/yellow]\n")

                    Path(os.path.dirname(routine_file)).mkdir(parents=True, exist_ok=True)
                    with open(routine_file, "w") as file:
                        lines = ["# Infomark Terminal CLI - Routine", "\n"]
                        username = getattr(session.user.profile.hub_session, "username", "local")
                        lines += [f"# Author: {username}", "\n\n"] if username else ["\n"]
                        lines += [
                            f"# Title: {SESSION_RECORDED_NAME}",
                            "\n",
                            f"# Tags: {SESSION_RECORDED_TAGS}",
                            "\n\n",
                            f"# Description: {SESSION_RECORDED_DESCRIPTION}",
                            "\n\n",
                        ]
                        lines += [c + "\n" for c in SESSION_RECORDED[:-1]]
                        file.writelines(lines)

                    session.console.print(f"[green]Routine saved at: {routine_file}[/green]\n")
                # If user doesn't specify they want to store routine locally
                # Confirm that the user is logged in
                elif not session.is_local():
                    routine = "\n".join(SESSION_RECORDED[:-1])
                    hub_session = current_user.profile.hub_session

                    if routine is not None:
                        auth_header = (
                            f"{hub_session.token_type} {hub_session.access_token.get_secret_value()}"
                            if hub_session
                            else None
                        )
                        kwargs = {
                            "auth_header": auth_header,
                            "name": SESSION_RECORDED_NAME,
                            "description": SESSION_RECORDED_DESCRIPTION,
                            "routine": routine,
                            "tags": SESSION_RECORDED_TAGS,
                            "public": SESSION_RECORDED_PUBLIC,
                        }
                        response = upload_routine(**kwargs)  # type: ignore
                        if response is not None and response.status_code == 409:
                            i = session.console.input(
                                "A routine with the same name already exists, "
                                "do you want to replace it? (y/n): "
                            )
                            session.console.print("")
                            if i.lower() in ["y", "yes"]:
                                kwargs["override"] = True  # type: ignore
                                response = upload_routine(**kwargs)  # type: ignore
                            else:
                                session.console.print("[info]Aborted.[/info]")

                # Clear session to be recorded again
                RECORD_SESSION = False
                SESSION_RECORDED = list()

    def call_whoami(self, other_args: List[str]) -> None:
        """Process whoami command."""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="whoami",
            description="Show current user",
        )
        ns_parser, _ = self.parse_simple_args(parser, other_args)

        if ns_parser:
            current_user = session.user
            local_user = session.is_local()
            if not local_user:
                hub_session = current_user.profile.hub_session
                session.console.print(
                    f"[info]email:[/info] {hub_session.email if hub_session else 'N/A'}"
                )
                session.console.print(
                    f"[info]uuid:[/info] {hub_session.user_uuid if hub_session else 'N/A'}"
                )
            else:
                print_guest_block_msg()

    def call_results(self, other_args: List[str]):
        """Process results command."""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="results",
            description="Process results command. This command displays a registry of "
            "'Infomark Objects' where all execution results are stored. "
            "It is organized as a stack, with the most recent result at index 0.",
        )
        parser.add_argument("--index", dest="index", help="Index of the result.")
        parser.add_argument("--key", dest="key", help="Key of the result.")
        parser.add_argument(
            "--chart", action="store_true", dest="chart", help="Display chart."
        )
        parser.add_argument(
            "--export",
            default="",
            type=check_file_type_saved(["csv", "json", "xlsx", "png", "jpg"]),
            dest="export",
            help="Export raw data into csv, json, xlsx and figure into png or jpg.",
            nargs="+",
        )
        parser.add_argument(
            "--sheet-name",
            dest="sheet_name",
            default=None,
            nargs="+",
            help="Name of excel sheet to save data to. Only valid for .xlsx files.",
        )

        ns_parser, unknown_args = self.parse_simple_args(
            parser, other_args, unknown_args=True
        )

        if ns_parser:
            kwargs = parse_unknown_args_to_dict(unknown_args)
            if not ns_parser.index and not ns_parser.key:
                results = session.infomark_object_registry.all
                if results:
                    df = pd.DataFrame.from_dict(results, orient="index")
                    print_rich_table(
                        df,
                        show_index=True,
                        index_name="stack index",
                        title="Infomark Object Results",
                    )
                else:
                    session.console.print("[info]No results found.[/info]")
            elif ns_parser.index:
                try:
                    index = int(ns_parser.index)
                    infomark_object = session.infomark_object_registry.get(index)
                    if infomark_object:
                        handle_infomark_object_display(
                            infomark_object=infomark_object,
                            chart=ns_parser.chart,
                            export=ns_parser.export,
                            sheet_name=ns_parser.sheet_name,
                            **kwargs,
                        )
                    else:
                        session.console.print(
                            f"[info]No result found at index {index}.[/info]"
                        )
                except ValueError:
                    session.console.print(
                        f"[red]Index must be an integer, not '{ns_parser.index}'.[/red]"
                    )
            elif ns_parser.key:
                infomark_object = session.infomark_object_registry.get(ns_parser.key)
                if infomark_object:
                    handle_infomark_object_display(
                        infomark_object=infomark_object,
                        chart=ns_parser.chart,
                        export=ns_parser.export,
                        sheet_name=ns_parser.sheet_name,
                        **kwargs,
                    )
                else:
                    session.console.print(
                        f"[info]No result found with key '{ns_parser.key}'.[/info]"
                    )

    @staticmethod
    def parse_simple_args(
        parser: argparse.ArgumentParser,
        other_args: List[str],
        unknown_args: bool = False,
    ) -> Tuple[Optional[argparse.Namespace], Optional[List[str]]]:
        """Parse list of arguments into the supplied parser.

        Parameters
        ----------
        parser: argparse.ArgumentParser
            Parser with predefined arguments
        other_args: List[str]
            List of arguments to parse
        unknown_args: bool
            Flag to indicate if unknown arguments should be returned

        Returns
        -------
        ns_parser: argparse.Namespace
            Namespace with parsed arguments
        l_unknown_args: List[str]
            List of unknown arguments
        """
        parser.add_argument(
            "-h", "--help", action="store_true", help="show this help message"
        )

        if session.settings.USE_CLEAR_AFTER_CMD:
            system_clear()

        try:
            (ns_parser, l_unknown_args) = parser.parse_known_args(other_args)
        except SystemExit:
            # In case the command has required argument that isn't specified
            session.console.print("\n")
            return None, None

        if ns_parser.help:
            txt_help = parser.format_help()
            session.console.print(f"[help]{txt_help}[/help]")
            return None, None

        if l_unknown_args and not unknown_args:
            session.console.print(
                f"The following args couldn't be interpreted: {l_unknown_args}\n"
            )
        return ns_parser, l_unknown_args

    @classmethod
    def parse_known_args_and_warn(
        cls,
        parser: argparse.ArgumentParser,
        other_args: List[str],
        export_allowed: Literal[
            "no_export", "raw_data_only", "figures_only", "raw_data_and_figures"
        ] = "no_export",
        raw: bool = False,
        limit: int = 0,
    ):
        """Parse list of arguments into the supplied parser.

        Parameters
        ----------
        parser: argparse.ArgumentParser
            Parser with predefined arguments
        other_args: List[str]
            list of arguments to parse
        export_allowed: Literal["no_export", "raw_data_only", "figures_only", "raw_data_and_figures"]
            Export options
        raw: bool
            Add the --raw flag
        limit: int
            Add a --limit flag with this number default

        Returns
        ----------
        ns_parser:
            Namespace with parsed arguments
        """
        parser.add_argument(
            "-h", "--help", action="store_true", help="show this help message"
        )
        if export_allowed != "no_export":
            choices_export = []
            help_export = "Does not export!"

            if export_allowed == "raw_data_only":
                choices_export = ["csv", "json", "xlsx"]
                help_export = "Export raw data into csv, json or xlsx."
            elif export_allowed == "figures_only":
                choices_export = ["png", "jpg"]
                help_export = "Export figure into png or jpg."
            else:
                choices_export = ["csv", "json", "xlsx", "png", "jpg"]
                help_export = (
                    "Export raw data into csv, json, xlsx and figure into png or jpg."
                )

            parser.add_argument(
                "--export",
                default="",
                type=check_file_type_saved(choices_export),
                dest="export",
                help=help_export,
                nargs="+",
            )

            # If excel is an option, add the sheet name
            if export_allowed in [
                "raw_data_only",
                "raw_data_and_figures",
            ]:
                parser.add_argument(
                    "--sheet-name",
                    dest="sheet_name",
                    default=None,
                    nargs="+",
                    help="Name of excel sheet to save data to. Only valid for .xlsx files.",
                )

        if raw:
            parser.add_argument(
                "--raw",
                dest="raw",
                action="store_true",
                default=False,
                help="Flag to display raw data",
            )
        if limit > 0:
            parser.add_argument(
                "-l",
                "--limit",
                dest="limit",
                default=limit,
                help="Number of entries to show in data.",
                type=check_positive,
            )

        parser.add_argument(
            "--register_infomark_object",
            dest="register_infomark_object",
            action="store_false",
            default=True,
            help="Flag to store data in the Infomark Object registry, True by default.",
        )
        parser.add_argument(
            "--register_key",
            dest="register_key",
            default="",
            help="Key to reference data in the Infomark Object registry.",
            type=validate_register_key,
        )

        if session.settings.USE_CLEAR_AFTER_CMD:
            system_clear()

        if "--help" in other_args or "-h" in other_args:
            txt_help = parser.format_help() + "\n"
            session.console.print(f"[help]{txt_help}[/help]")
            return None

        try:
            # Determine the index of the routine arguments
            routine_args_index = next(
                (
                    i + 1
                    for i, arg in enumerate(other_args)
                    if arg in ("-i", "--input")
                    and "routine_args"
                    in [
                        action.dest
                        for action in parser._actions  # pylint: disable=protected-access
                    ]
                ),
                -1,
            )
            # Split comma-separated arguments, except for the argument at routine_args_index
            other_args = [
                part
                for index, arg in enumerate(other_args)
                for part in (arg.split(",") if index != routine_args_index else [arg])
            ]

            # Check if the action has optional choices, if yes, remove them
            for action in parser._actions:  # pylint: disable=protected-access
                if hasattr(action, "optional_choices") and action.optional_choices:
                    action.choices = None

            (ns_parser, l_unknown_args) = parser.parse_known_args(other_args)

            if export_allowed in [
                "raw_data_only",
                "raw_data_and_figures",
            ]:
                ns_parser.is_image = any(
                    ext in ns_parser.export for ext in ["png", "jpg"]
                )

        except SystemExit:
            # In case the command has required argument that isn't specified
            return None

        if l_unknown_args:
            session.console.print(
                f"The following args couldn't be interpreted: {l_unknown_args}"
            )
        return ns_parser

    def menu(self, custom_path_menu_above: str = ""):
        """Enter controller menu."""
        settings = session.settings
        an_input = "HELP_ME"

        while True:
            # There is a command in the queue
            if self.queue and len(self.queue) > 0:
                if self.queue[0] in ("q", "..", "quit"):
                    self.save_class()
                    # Go back to the root in order to go to the right directory because
                    # there was a jump between indirect menus
                    if custom_path_menu_above:
                        self.queue.insert(1, custom_path_menu_above)

                    if len(self.queue) > 1:
                        return self.queue[1:]

                    if settings.ENABLE_EXIT_AUTO_HELP:
                        return ["help"]
                    return []

                # Consume 1 element from the queue
                an_input = self.queue[0]
                self.queue = self.queue[1:]

                # Print location because this was an instruction and we want user to know the action
                if (
                    an_input
                    and an_input != "home"
                    and an_input != "help"
                    and an_input.split(" ")[0] in self.controller_choices
                ):
                    session.console.print(
                        f"{get_flair_and_username()} {self.PATH} $ {an_input}"
                    )

            # Get input command from user
            else:
                # Display help menu when entering on this menu from a level above
                if an_input == "HELP_ME":
                    self.print_help()

                try:
                    prompt_session = session.prompt_session
                    if prompt_session and settings.USE_PROMPT_TOOLKIT:
                        # Check if toolbar hint was enabled
                        if settings.TOOLBAR_HINT:
                            an_input = prompt_session.prompt(
                                f"{get_flair_and_username()} {self.PATH} $ ",
                                completer=self.completer,
                                search_ignore_case=True,
                                bottom_toolbar=HTML(
                                    '<style bg="ansiblack" fg="ansiwhite">[h]</style> help menu    '
                                    '<style bg="ansiblack" fg="ansiwhite">[q]</style> return to previous menu    '
                                    '<style bg="ansiblack" fg="ansiwhite">[e]</style> exit the program    '
                                    '<style bg="ansiblack" fg="ansiwhite">[cmd -h]</style> '
                                    "see usage and available options    "
                                    f"{self.path[-1].capitalize()} (cmd/menu) Documentation"
                                ),
                                style=Style.from_dict(
                                    {"bottom-toolbar": "#ffffff bg:#333333"}
                                ),
                            )
                        else:
                            an_input = prompt_session.prompt(
                                f"{get_flair_and_username()} {self.PATH} $ ",
                                completer=self.completer,
                                search_ignore_case=True,
                            )
                    # Get input from user without auto-completion
                    else:
                        an_input = input(f"{get_flair_and_username()} {self.PATH} $ ")

                except (KeyboardInterrupt, EOFError):
                    # Exit in case of keyboard interrupt
                    an_input = "exit"

            try:
                # Allow user to go back to root
                an_input = "home" if an_input == "/" else an_input

                # Process the input command
                self.queue = self.switch(an_input)

            except SystemExit:
                session.console.print(
                    f"[red]The command '{an_input}' doesn't exist on the {self.PATH} menu.[/red]\n",
                )
                similar_cmd = difflib.get_close_matches(
                    an_input.split(" ")[0] if " " in an_input else an_input,
                    self.controller_choices,
                    n=1,
                    cutoff=0.7,
                )
                if similar_cmd:
                    if " " in an_input:
                        candidate_input = (
                            f"{similar_cmd[0]} {' '.join(an_input.split(' ')[1:])}"
                        )
                        if candidate_input == an_input:
                            an_input = ""
                            self.queue = []
                            session.console.print("\n")
                            continue

                        an_input = candidate_input
                    else:
                        an_input = similar_cmd[0]

                    session.console.print(
                        f"[green]Replacing by '{an_input}'.[/green]\n"
                    )
                    self.queue.insert(0, an_input)
