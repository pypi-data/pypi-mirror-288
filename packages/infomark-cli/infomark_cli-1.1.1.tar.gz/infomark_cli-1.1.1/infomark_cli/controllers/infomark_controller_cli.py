#!/usr/bin/env python
"""Main CLI Module."""

import argparse
import contextlib
import difflib
import os
import re
import sys
import time
import webbrowser
from datetime import datetime
from functools import partial, update_wrapper
from pathlib import Path
from types import MethodType
from typing import Any, Dict, List, Optional

import pandas as pd
import requests

from infomark import imb
from infomark_cli.config import constants
from infomark_cli.config.constants import (
    ASSETS_DIRECTORY,
    ENV_FILE_SETTINGS,
    HOME_DIRECTORY,
    REPOSITORY_DIRECTORY,
)
from infomark_cli.config.menu_text import MenuText
from infomark_cli.controllers.base_controller import BaseController
from infomark_cli.controllers.platform_controller_factory import (
    PlatformControllerFactory,
)
from infomark_cli.controllers.script_parser import is_reset, parse_infomark_script
from infomark_cli.controllers.utils import (
    bootup,
    first_time_user,
    get_flair_and_username,
    parse_and_split_input,
    print_goodbye,
    print_rich_table,
    reset,
    suppress_stdout,
    welcome_message,
)
from infomark_cli.session import Session
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style
from pydantic import BaseModel

PLATFORM_ROUTERS = {
    d: "menu" if not isinstance(getattr(imb, d), BaseModel) else "command"
    for d in dir(imb)
    if "_" not in d
}
NON_DATA_ROUTERS = ["coverage", "account", "reference", "system", "user"]
DATA_PROCESSING_ROUTERS = ["technical", "quantitative", "econometrics"]

# pylint: disable=too-many-public-methods,import-outside-toplevel, too-many-function-args
# pylint: disable=too-many-branches,no-member,C0302,too-many-return-statements, inconsistent-return-statements

env_file = str(ENV_FILE_SETTINGS)
session = Session()


class CLIController(BaseController):
    """CLI Controller class."""

    CHOICES_COMMANDS = ["record", "stop", "exe", "results"]
    CHOICES_MENUS = [
        "settings",
    ]

    for router, value in PLATFORM_ROUTERS.items():
        if value == "menu":
            CHOICES_MENUS.append(router)
        else:
            CHOICES_COMMANDS.append(router)

    PATH = "/"
    CHOICES_GENERATION = False

    def __init__(self, jobs_cmds: Optional[List[str]] = None):
        """Construct CLI controller."""
        self.ROUTINE_FILES: Dict[str, str] = dict()
        self.ROUTINE_DEFAULT_FILES: Dict[str, str] = dict()
        self.ROUTINE_PERSONAL_FILES: Dict[str, str] = dict()
        self.ROUTINE_CHOICES: Dict[str, Any] = dict()

        super().__init__(jobs_cmds)

        self.queue: List[str] = list()

        if jobs_cmds:
            self.queue = parse_and_split_input(
                an_input=" ".join(jobs_cmds), custom_filters=[]
            )

        self.update_success = False

        self._generate_platform_commands()

        self.update_runtime_choices()

    def _generate_platform_commands(self):
        """Generate Platform based commands/menus."""

        def method_call_class(self, _, controller, name, parent_path, target):
            self.queue = self.load_class(
                controller, name, parent_path, target, self.queue
            )

        # pylint: disable=unused-argument
        def method_call_command(self, _, router: str):
            """Call command."""
            mdl = getattr(imb, router)
            df = pd.DataFrame.from_dict(mdl.model_dump(), orient="index")
            if isinstance(df.columns, pd.RangeIndex):
                df.columns = [str(i) for i in df.columns]
            return print_rich_table(df, show_index=True)

        for router, value in PLATFORM_ROUTERS.items():
            target = getattr(imb, router)

            if value == "menu":
                pcf = PlatformControllerFactory(
                    target, reference=imb.reference["paths"]  # type: ignore
                )
                DynamicController = pcf.create()

                # Bind the method to the class
                bound_method = MethodType(method_call_class, self)

                # Update the wrapper and set the attribute
                bound_method = update_wrapper(  # type: ignore
                    partial(
                        bound_method,
                        controller=DynamicController,
                        name=router,
                        target=target,
                        parent_path=self.path,
                    ),
                    method_call_class,
                )
            else:
                bound_method = MethodType(method_call_command, self)
                bound_method = update_wrapper(  # type: ignore
                    partial(bound_method, router=router),
                    method_call_command,
                )

            setattr(self, f"call_{router}", bound_method)

    def update_runtime_choices(self):
        """Update runtime choices."""
        routines_directory = Path(session.user.preferences.export_directory, "routines")

        if session.prompt_session and session.settings.USE_PROMPT_TOOLKIT:
            # choices: dict = self.choices_default
            choices: dict = {c: {} for c in self.controller_choices}  # type: ignore

            self.ROUTINE_FILES = {
                filepath.name: filepath  # type: ignore
                for filepath in routines_directory.rglob("*.infomark")
            }
            self.ROUTINE_DEFAULT_FILES = {
                filepath.name: filepath  # type: ignore
                for filepath in Path(routines_directory / "hub" / "default").rglob(
                    "*.infomark"
                )
            }
            self.ROUTINE_PERSONAL_FILES = {
                filepath.name: filepath  # type: ignore
                for filepath in Path(routines_directory / "hub" / "personal").rglob(
                    "*.infomark"
                )
            }

            choices["exe"] = {
                "--file": {
                    filename: {} for filename in list(self.ROUTINE_FILES.keys())
                },
                "-f": "--file",
                "--example": None,
                "-e": "--example",
                "--input": None,
                "-i": "--input",
                "--url": None,
                "--help": None,
                "-h": "--help",
            }
            choices["record"] = {
                "--name": None,
                "-n": "--name",
                "--description": None,
                "-d": "--description",
                "--public": None,
                "-p": "--public",
                "--tag1": {c: None for c in constants.SCRIPT_TAGS},
                "--tag2": {c: None for c in constants.SCRIPT_TAGS},
                "--tag3": {c: None for c in constants.SCRIPT_TAGS},
                "--help": None,
                "-h": "--help",
            }
            choices["stop"] = {"--help": None, "-h": "--help"}
            choices["results"] = {
                "--help": None,
                "-h": "--help",
                "--export": {c: None for c in ["csv", "json", "xlsx", "png", "jpg"]},
                "--index": None,
                "--key": None,
                "--chart": None,
                "--sheet_name": None,
            }

            self.update_completer(choices)

    def print_help(self):
        """Print help."""
        mt = MenuText("")

        mt.add_info("Configure the platform and manage your account")
        for router, value in PLATFORM_ROUTERS.items():
            if router not in NON_DATA_ROUTERS or router in ["reference", "coverage"]:
                continue
            if value == "menu":
                menu_description = (
                    imb.reference["routers"]  # type: ignore
                    .get(f"{self.PATH}{router}", {})
                    .get("description")
                ) or ""
                mt.add_menu(
                    name=router,
                    description=menu_description.split(".")[0].lower(),
                )            else:
                mt.add_cmd(router)

        mt.add_info("\nConfigure your CLI")
        mt.add_menu(
            "settings",
            description="enable and disable feature flags, preferences and settings",
        )
        mt.add_raw("\n")
        mt.add_info("Record and execute your own .infomark routine scripts")
        mt.add_cmd("record", description="start recording current session")
        mt.add_cmd(
            "stop", description="stop session recording and convert to .infomark routine"
        )
        mt.add_cmd(
            "exe",
            description="execute .infomark routine scripts (use exe --example for an example)",
        )
        mt.add_raw("\n")
        mt.add_info("Retrieve data from different asset classes and providers")

        for router, value in PLATFORM_ROUTERS.items():
            if router in NON_DATA_ROUTERS or router in DATA_PROCESSING_ROUTERS:
                continue
            if value == "menu":
                menu_description = (
                    imb.reference["routers"]  # type: ignore
                    .get(f"{self.PATH}{router}", {})
                    .get("description")
                ) or ""
                mt.add_menu(
                    name=router,
                    description=menu_description.split(".")[0].lower(),
                )
            else:
                mt.add_cmd(router)

        if any(router in PLATFORM_ROUTERS for router in DATA_PROCESSING_ROUTERS):
            mt.add_info("\nAnalyze and process previously obtained data")

            for router, value in PLATFORM_ROUTERS.items():
                if router not in DATA_PROCESSING_ROUTERS:
                    continue
                if value == "menu":
                    menu_description = (
                        imb.reference["routers"]  # type: ignore
                        .get(f"{self.PATH}{router}", {})
                        .get("description")
                    ) or ""
                    mt.add_menu(
                        name=router,
                        description=menu_description.split(".")[0].lower(),
                    )
                else:
                    mt.add_cmd(router)

        mt.add_raw("\n")
        mt.add_cmd("results")
        if session.imbject_registry.imbjects:
            mt.add_info("\nCached Results")
            for key, value in list(session.imbject_registry.all.items())[  # type: ignore
                : session.settings.N_TO_DISPLAY_IMBJECT_REGISTRY
            ]:
                mt.add_raw(
                    f"[yellow]IMB{key}[/yellow]: {value['command']}",  # type: ignore[index]
                    left_spacing=True,
                )

        session.console.print(text=mt.menu_text, menu="Home")
        self.update_runtime_choices()

    def parse_input(self, an_input: str) -> List:
        """Overwrite the BaseController parse_input for `askimb` and 'exe'.

        This will allow us to search for something like "P/E" ratio.
        """
        # Filtering out sorting parameters with forward slashes like P/E
        sort_filter = r"((\ -q |\ --question|\ ).*?(/))"
        # Filter out urls
        url = r"(exe (--url )?(https?://)?my\.infomark\.(dev|co)/u/.*/routine/.*)"
        custom_filters = [sort_filter, url]
        return parse_and_split_input(an_input=an_input, custom_filters=custom_filters)

    def call_settings(self, _):
        """Process settings command."""
        from infomark_cli.controllers.settings_controller import (
            SettingsController,
        )

        self.queue = self.load_class(SettingsController, self.queue)

    def call_exe(self, other_args: List[str]):
        """Process exe command."""
        # Merge rest of string path to other_args and remove queue since it is a dir
        other_args += self.queue

        if not other_args:
            session.console.print(
                "[info]Provide a path to the routine you wish to execute. For an example, please use "
                "`exe --example`.\n[/info]"
            )
            return
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="exe",
            description="Execute automated routine script. For an example, please use "
            "`exe --example`.",
        )
        parser.add_argument(
            "--file",
            "-f",
            help="The path or .infomark file to run.",
            dest="file",
            required="-h" not in other_args
            and "--help" not in other_args
            and "-e" not in other_args
            and "--example" not in other_args
            and "--url" not in other_args
            and "my.infomark" not in other_args[0],
            type=str,
            nargs="+",
        )
        parser.add_argument(
            "-i",
            "--input",
            help="Select multiple inputs to be replaced in the routine and separated by commas. E.g. GME,AMC,BTC-USD",
            dest="routine_args",
            type=str,
        )
        parser.add_argument(
            "-e",
            "--example",
            help="Run an example script to understand how routines can be used.",
            dest="example",
            action="store_true",
            default=False,
        )
        parser.add_argument(
            "--url", help="URL to run infomark script from.", dest="url", type=str
        )
        if other_args and "-" not in other_args[0][0]:
            if other_args[0].startswith("my.") or other_args[0].startswith("http"):
                other_args.insert(0, "--url")
            else:
                other_args.insert(0, "--file")
        ns_parser = self.parse_known_args_and_warn(parser, other_args)
        if ns_parser:
            if ns_parser.example:
                routine_path = ASSETS_DIRECTORY / "routines" / "routine_example.infomark"
                session.console.print(  # TODO: Point to docs when ready
                    "[info]Executing an example, please visit our docs "
                    "to learn how to create your own script.[/info]\n"
                )
                time.sleep(3)
            elif ns_parser.url:
                if not ns_parser.url.startswith(
                    "https"
                ) and not ns_parser.url.startswith("http:"):
                    url = "https://" + ns_parser.url
                elif ns_parser.url.startswith("http://"):
                    url = ns_parser.url.replace("http://", "https://")
                else:
                    url = ns_parser.url
                username = url.split("/")[-3]
                script_name = url.split("/")[-1]
                file_name = f"{username}_{script_name}.infomark"
                final_url = f"{url}?raw=true"
                response = requests.get(final_url, timeout=10)
                if response.status_code != 200:
                    session.console.print(
                        "[red]Could not find the requested script.[/red]"
                    )
                    return
                routine_text = response.json()["script"]
                file_path = Path(session.user.preferences.export_directory, "routines")
                routine_path = file_path / file_name
                with open(routine_path, "w") as file:
                    file.write(routine_text)
                self.update_runtime_choices()

            elif ns_parser.file:
                file_path = " ".join(ns_parser.file)  # type: ignore
                # if string is not in this format "default/file.infomark" then check for files in ROUTINE_FILES
                full_path = file_path
                hub_routine = file_path.split("/")  # type: ignore
                # Change with: my.infomark.co
                if hub_routine[0] == "default":
                    routine_path = Path(
                        self.ROUTINE_DEFAULT_FILES.get(hub_routine[1], full_path)
                    )
                elif hub_routine[0] == "personal":
                    routine_path = Path(
                        self.ROUTINE_PERSONAL_FILES.get(hub_routine[1], full_path)
                    )
                else:
                    routine_path = Path(self.ROUTINE_FILES.get(file_path, full_path))  # type: ignore
            else:
                return

            try:
                with open(routine_path) as fp:
                    raw_lines = list(fp)

                script_inputs = []
                # Capture ARGV either as list if args separated by commas or as single value
                if routine_args := ns_parser.routine_args:
                    pattern = r"\[(.*?)\]"
                    matches = re.findall(pattern, routine_args)

                    for match in matches:
                        routine_args = routine_args.replace(f"[{match}]", "")
                        script_inputs.append(match)

                    script_inputs.extend(
                        [val for val in routine_args.split(",") if val]
                    )

                err, parsed_script = parse_infomark_script(
                    raw_lines=raw_lines, script_inputs=script_inputs
                )
# Handle errors in parsing and avoid processing faulty data
if err:
    session.console.print(err)
    return

# Convert parsed script into a command queue, filtering out empty values
self.queue = [
    command
    for command in parse_and_split_input(an_input=parsed_script, custom_filters=[])
    if command
]

# Manage the export path if specified
if "export" in self.queue[0]:
    export_path = self.queue[0].split(" ")[1]
    # Convert the path to an absolute path if it starts with ~ or is relative
    if export_path.startswith("~"):
        export_path = export_path.replace("~", HOME_DIRECTORY.as_posix())
    elif not export_path.startswith("/"):
        export_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), export_path
        )

    # Create directory if it does not exist
    if os.path.isdir(export_path):
        session.console.print(
            f"Data will be exported to the folder: '{export_path}'"
        )
    else:
        os.makedirs(export_path)
        session.console.print(
            f"[green]Successfully created folder '{export_path}'.[/green]"
        )
    self.queue = self.queue[1:]

# Handle case where file is not found
except FileNotFoundError:
    session.console.print(
        f"[red]File '{routine_path}' not found.[/red]"
    )
    return

def process_job_commands(jobs_cmds: Optional[List[str]]) -> Optional[List[str]]:
    """Process job commands, particularly for export functionality."""
    export_path = ""
    if jobs_cmds and "export" in jobs_cmds[0]:
        command_parts = jobs_cmds[0].split("/")
        initial_split = command_parts[0].split(" ")
        if len(initial_split) > 1:
            export_path = initial_split[1]
        jobs_cmds = ["/".join(command_parts[1:])]
    
    if not export_path:
        return jobs_cmds

    # Adjust export path if it starts with ~ or is relative
    if export_path.startswith("~"):
        export_path = export_path.replace("~", HOME_DIRECTORY.as_posix())
    elif not export_path.startswith("/"):
        export_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), export_path
        )

    # Create the directory if it does not exist
    if os.path.isdir(export_path):
        session.console.print(
            f"Data will be exported to the folder: '{export_path}'"
        )
    else:
        os.makedirs(export_path)
        session.console.print(
            f"[green]Successfully created folder '{export_path}'.[/green]"
        )
    return jobs_cmds

# pylint: disable=unused-argument
def execute_cli(jobs_cmds: Optional[List[str]] = None, test_mode=False):
    """Execute the CLI interface."""
    exit_code = 1
    controller = CLIController(jobs_cmds)
    user_input = ""

    jobs_cmds = process_job_commands(jobs_cmds)

    bootup()
    if not jobs_cmds:
        display_welcome_message()

        if is_first_time_user():
            with contextlib.suppress(EOFError):
                webbrowser.open("https://docs.infomark.co/cli")

        controller.display_help()

    while exit_code:
        # If there are commands in the queue
        if controller.queue and len(controller.queue) > 0:
            # If the command is to quit, exit the loop
            if controller.queue[0] in ("q", "..", "quit"):
                display_goodbye_message()
                break

            # Process one command from the queue
            user_input = controller.queue[0]
            controller.queue = controller.queue[1:]

            # Print the command and its current status
            if user_input and user_input.split(" ")[0] in controller.CHOICES_COMMANDS:
                session.console.print(f"{get_user_flair()} / $ {user_input}")

        # Prompt user for input
        else:
            try:
                # Get input with auto-completion if enabled
                if session.prompt_session and session.settings.ENABLE_PROMPT_TOOLKIT:
                    if session.settings.SHOW_TOOLBAR_HINT:
                        user_input = session.prompt_session.prompt(  # type: ignore[union-attr]
                            f"{get_user_flair()} / $ ",
                            completer=controller.completer,
                            search_ignore_case=True,
                            bottom_toolbar=HTML(
                                '<style bg="ansiblack" fg="ansiwhite">[h]</style> help menu    '
                                '<style bg="ansiblack" fg="ansiwhite">[q]</style> return to previous menu    '
                                '<style bg="ansiblack" fg="ansiwhite">[e]</style> exit the program    '
                                '<style bg="ansiblack" fg="ansiwhite">[cmd -h]</style> '
                                "view usage and options    "
                            ),
                            style=Style.from_dict(
                                {
                                    "bottom-toolbar": "#ffffff bg:#333333",
                                }
                            ),
                        )
                    else:
                        user_input = session.prompt_session.prompt(  # type: ignore[union-attr]
                            f"{get_user_flair()} / $ ",
                            completer=controller.completer,
                            search_ignore_case=True,
                        )

                # Get input without auto-completion
                else:
                    user_input = input(f"{get_user_flair()} / $ ")

            except (KeyboardInterrupt, EOFError):
                display_goodbye_message()
                break

        try:
            # Process the user input command
            controller.queue = controller.switch(user_input)

            if user_input in ("q", "quit", "..", "exit", "e"):
                display_goodbye_message()
                break

            # Check if the user wants to reset the application
            if user_input in ("r", "reset") or controller.update_success:
                reset_application(controller.queue if controller.queue else [])
                break

        except SystemExit:
            session.console.print(
                f"[red]The command '{user_input}' is not recognized in the / menu.[/red]\n",
            )
            similar_command = difflib.get_close_matches(
                user_input.split(" ")[0] if " " in user_input else user_input,
                controller.controller_choices,
                n=1,
                cutoff=0.7,
            )
            if similar_command:
                user_input = similar_command[0]
                if " " in user_input:
                    adjusted_input = (
                        f"{similar_command[0]} {' '.join(user_input.split(' ')[1:])}"
                    )
                    if adjusted_input == user_input:
                        user_input = ""
                        controller.queue = []
                        session.console.print("\n")
                        continue
                    user_input = adjusted_input

                session.console.print(f"[green]Replacing with '{user_input}'.[/green]")
                controller.queue.insert(0, user_input)

def prepend_slash_to_commands(cmds: List[str]) -> List[str]:
    """Add a leading slash to a command sequence if not present."""
    if not cmds[0].startswith("/"):
        cmds[0] = f"/{cmds[0]}"
    if cmds[0].startswith("/home"):
        cmds[0] = f"/{cmds[0][5:]}"
    return cmds
import os
import re
import sys
import argparse
import contextlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Constants
HOME_DIRECTORY = Path.home()
REPOSITORY_DIRECTORY = Path(__file__).parent
ASSETS_DIRECTORY = REPOSITORY_DIRECTORY / "assets"

def run_scripts(
    path: Path,
    test_mode: bool = False,
    verbose: bool = False,
    routines_args: Optional[List[str]] = None,
    special_arguments: Optional[Dict[str, str]] = None,
    output: bool = True,
):
    """Execute the given scripts with .OpenBB extension.

    Parameters
    ----------
    path : Path
        The location of the .OpenBB file
    test_mode : bool
        Whether the CLI is running in test mode
    verbose : bool
        Whether to run tests with detailed output
    routines_args : Optional[List[str]]
        Arguments to replace in the routine
    special_arguments : Optional[Dict[str, str]]
        Arguments to replace in the script using a dictionary
    output : bool
        Whether to log the output to text files
    """
    if not path.exists():
        session.console.print(f"File '{path}' not found. Launching default CLI.\n")
        if not test_mode:
            run_cli()

    # Open and process the script file
    with path.open() as fp:
        raw_lines = [line for line in fp if (not is_reset(line)) and ("#" not in line) and line]
        raw_lines = [line.strip() for line in raw_lines if line.strip()]

        # Replace routine arguments if provided
        if routines_args:
            lines = [
                line.replace(f"$ARGV[{i}]", arg)
                for i, arg in enumerate(routines_args)
                for line in raw_lines
            ]
        # Replace special arguments if provided
        elif special_arguments:
            lines = [
                re.sub(
                    r"\${[^{]+=[^{]+}",
                    lambda match: replace_dynamic(match, special_arguments),
                    line,
                )
                for line in raw_lines
            ]
        else:
            lines = raw_lines

        # Append exit command if in test mode
        if test_mode and "exit" not in lines[-1]:
            lines.append("exit")

        # Handle export folder if specified
        export_folder = ""
        if "export" in lines[0]:
            export_folder = lines[0].split("export ")[1].strip()
            lines = lines[1:]

        simulate_argv = f"/{'/'.join([line.rstrip() for line in lines])}"
        file_cmds = simulate_argv.replace("//", "/home/").split()
        file_cmds = insert_start_slash(file_cmds) if file_cmds else file_cmds
        file_cmds = (
            [f"export {export_folder} {' '.join(file_cmds)}"]
            if export_folder
            else [" ".join(file_cmds)]
        )

        # Execute CLI commands
        if not test_mode or verbose:
            run_cli(file_cmds, test_mode=True)
        else:
            with suppress_stdout():
                session.console.print(f"Output will be logged: {output}")
                if output:
                    timestamp = datetime.now().timestamp()
                    stamp_str = str(timestamp).replace(".", "")
                    output_path = Path(REPOSITORY_DIRECTORY / "integration_test_output")
                    output_path.mkdir(parents=True, exist_ok=True)
                    first_cmd = file_cmds[0].split("/")[1]
                    with open(
                        output_path / f"{stamp_str}_{first_cmd}_output.txt", "w"
                    ) as output_file, contextlib.redirect_stdout(output_file):
                        run_cli(file_cmds, test_mode=True)
                else:
                    run_cli(file_cmds, test_mode=True)


def replace_dynamic(match: re.Match, special_arguments: Dict[str, str]) -> str:
    """Replace ${key=default} with value from special_arguments or default.

    Parameters
    ----------
    match : re.Match
        The match object
    special_arguments : Dict[str, str]
        Key-value pairs for replacement

    Returns
    -------
    str
        The replaced string
    """
    cleaned = match.group(0).strip("${}").replace("$", "")
    key, default = cleaned.split("=")
    return special_arguments.get(key, default)


def run_routine(file: str, routines_args: Optional[List[str]] = None):
    """Execute a command routine from an .OpenBB file."""
    user_routine_path = Path(session.user.preferences.export_directory, "routines")
    default_routine_path = ASSETS_DIRECTORY / "routines" / file

    if user_routine_path.exists():
        run_scripts(path=user_routine_path, routines_args=routines_args)
    elif default_routine_path.exists():
        run_scripts(path=default_routine_path, routines_args=routines_args)
    else:
        session.console.print(
            f"Routine not found. Place your .OpenBB file in: {user_routine_path}."
        )


# pylint: disable=unused-argument
def main(
    debug: bool,
    dev: bool,
    path_list: List[str],
    routines_args: Optional[List[str]] = None,
    **kwargs,
):
    """Run the CLI with various configurations.

    Parameters
    ----------
    debug : bool
        Whether to enable debug mode
    dev : bool
        Whether to use the development backend
    path_list : List[str]
        Paths to scripts or commands to execute
    routines_args : Optional[List[str]]
        Arguments for the routines
    """
    if debug:
        session.settings.DEBUG_MODE = True

    if dev:
        session.settings.DEV_BACKEND = True
        session.settings.BASE_URL = "https://payments.infomark.dev/"
        session.settings.HUB_URL = "https://my.infomark.dev"

    if isinstance(path_list, list) and path_list[0].endswith(".OpenBB"):
        run_routine(file=path_list[0], routines_args=routines_args)
    elif path_list:
        argv_cmds = [" ".join(path_list).replace(" /", "/home/")]
        argv_cmds = insert_start_slash(argv_cmds) if argv_cmds else argv_cmds
        run_cli(argv_cmds)
    else:
        run_cli()


def parse_args_and_run():
    """Parse command-line arguments and execute CLI."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog="cli",
        description="The Infomark Platform CLI.",
    )
    parser.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="Enable debug mode.",
    )
    parser.add_argument(
        "--dev",
        dest="dev",
        action="store_true",
        default=False,
        help="Use development environment instead of production.",
    )
    parser.add_argument(
        "--file",
        help="Path to the .OpenBB file to execute.",
        dest="path",
        nargs="+",
        default="",
        type=str,
    )
    parser.add_argument(
        "-i",
        "--input",
        help="Arguments to be replaced in the routine, separated by commas (e.g., GME,AMC,BTC-USD).",
        dest="routine_args",
        type=lambda s: [str(item) for item in s.split(",")],
        default=None,
    )
    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        help="Run CLI in testing mode. Use with '-h' for help on testing options.",
    )
    # Arguments for reports menu
    parser.add_argument(
        "-m",
        help=argparse.SUPPRESS,
        dest="module",
        default="",
        type=str,
    )
    parser.add_argument(
        "-f",
        help=argparse.SUPPRESS,
        dest="module_file",
        default="",
        type=str,
    )
    parser.add_argument(
        "--HistoryManager.hist_file",
        help=argparse.SUPPRESS,
        dest="module_hist_file",
        default="",
        type=str,
    )
    if sys.argv[1:] and "-" not in sys.argv[1][0]:
        sys.argv.insert(1, "--file")
    ns_parser, unknown = parser.parse_known_args()

    # Exit if unknown args are present and not in debug mode
    if unknown:
        if ns_parser.debug:
            session.console.print(unknown)
        else:
            sys.exit(-1)

    main(
        ns_parser.debug,
        ns_parser.dev,
        ns_parser.path,
        ns_parser.routine_args,
        module=ns_parser.module,
        module_file=ns_parser.module_file,
        module_hist_file=ns_parser.module_hist_file,
    )


def launch(
    debug: bool = False, dev: bool = False, queue: Optional[List[str]] = None
) -> None:
    """Start the CLI."""
    if queue:
        main(debug, dev, queue, module="")
    else:
        parse_args_and_run()


if __name__ == "__main__":
    parse_args_and_run()


