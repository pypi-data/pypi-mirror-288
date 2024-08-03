"""This module provides utilities for constructing the choice map for controllers."""

from argparse import SUPPRESS, ArgumentParser
from contextlib import contextmanager
from inspect import isfunction, unwrap
from types import MethodType
from typing import Callable, List, Literal, Tuple
from unittest.mock import patch

from infomark_cli.controllers.utils import (
    validate_file_type,
    ensure_positive,
    validate_key_format,
)
from infomark_cli.session import Session

session = Session()


def mock_parse_arguments(
    controller,  # pylint: disable=unused-argument
    parser: ArgumentParser,
    extra_args: List[str],
    export_mode: Literal[
        "none", "data_only", "figures_only", "data_and_figures"
    ] = "none",
    raw_output: bool = False,
    entry_limit: int = 0,
) -> None:
    """Add arguments to the parser.

    Mimics the argument addition from:
        - infomark_cli.base_controller.BaseController.parse_known_args_and_warn

    Parameters
    ----------
    parser: argparse.ArgumentParser
        The argument parser to which arguments are added.
    extra_args: List[str]
        Additional arguments to parse.
    export_mode: Literal["none", "data_only", "figures_only", "data_and_figures"]
            Options for exporting data.
    raw_output: bool
        Add the --raw flag for raw output.
    entry_limit: int
        Limit the number of entries displayed.
    """
    _ = extra_args

    parser.add_argument(
        "-h", "--help", action="store_true", help="Display help message"
    )

    if export_mode != "none":
        export_choices = []
        export_help = "Export options are not available."

        if export_mode == "data_only":
            export_choices = ["csv", "json", "xlsx"]
            export_help = "Export data in csv, json, or xlsx format."
        elif export_mode == "figures_only":
            export_choices = ["png", "jpg"]
            export_help = "Export figures in png or jpg format."
        else:
            export_choices = ["csv", "json", "xlsx", "png", "jpg"]
            export_help = (
                "Export data in csv, json, xlsx and figures in png or jpg."
            )

        parser.add_argument(
            "--export",
            default="",
            type=validate_file_type(export_choices),
            dest="export",
            help=export_help,
            choices=export_choices,
        )

    if raw_output:
        parser.add_argument(
            "--raw",
            dest="raw",
            action="store_true",
            default=False,
            help="Flag to display raw data",
        )
    if entry_limit > 0:
        parser.add_argument(
            "-l",
            "--limit",
            dest="limit",
            default=entry_limit,
            help="Number of entries to display.",
            type=ensure_positive,
        )

    parser.add_argument(
        "--register_infomark",
        dest="register_infomark",
        action="store_false",
        default=True,
        help="Flag to store data in the Infomark registry, enabled by default.",
    )
    parser.add_argument(
        "--register_key",
        dest="register_key",
        default="",
        help="Key for referencing data in the Infomark registry.",
        type=validate_key_format,
    )


def mock_parse_arguments_simple(parser: ArgumentParser, extra_args: List[str]) -> Tuple:
    """Add basic arguments.

    Mimics the addition of basic arguments from:
        - infomark_cli.parent_classes.BaseController.parse_simple_args

    Parameters
    ----------
    parser: argparse.ArgumentParser
        The argument parser to which arguments are added.
    extra_args: List[str]
        Additional arguments to parse.
    """
    parser.add_argument(
        "-h", "--help", action="store_true", help="Display help message"
    )
    _ = extra_args
    return None, None


def fetch_command_function(controller, command_name: str):
    """Retrieve the command function named `f"call_{command_name}"` from the controller.

    Parameters
    ----------
    controller: BaseController
        The CLI Controller instance.
    command_name: str
        Command name from controller.CHOICES_COMMANDS.

    Returns
    -------
    Callable: The command function.
    """
    if command_name not in controller.CHOICES_COMMANDS:
        raise AttributeError(
            f"Command '{command_name}' is not in `CHOICES_COMMANDS`."
        )

    command_function_name = f"call_{command_name}"
    command_function = getattr(controller, command_function_name)
    command_function = unwrap(func=command_function)

    if isfunction(command_function):
        command_function = MethodType(command_function, controller)

    return command_function


def has_patchable_functions(command_function: Callable) -> bool:
    """Verify if the command function contains mockable functions.

    Parameters
    ----------
    command_function: Callable
        The function to check.

    Returns
    -------
    bool: Whether the function includes parse_simple_args or parse_known_args_and_warn.
    """
    function_names = command_function.__code__.co_names

    return "parse_simple_args" in function_names or "parse_known_args_and_warn" in function_names


@contextmanager
def patch_controller_methods(controller):
    """Patch specific methods of the controller.

    Patch the following methods from a BaseController instance:
        - parse_simple_args
        - parse_known_args_and_warn

    Parameters
    ----------
    controller: BaseController
        The controller object to be patched.

    Returns
    -------
    List[Callable]: List of patched functions.
    """
    mock_parse_known_args_and_warn_bound = MethodType(
        mock_parse_arguments,
        controller,
    )

    print_patch = patch(
        target="infomark_cli.config.console.Console.print",
        return_value=None,
    )

    patchers = [
        patch.object(
            target=controller,
            attribute="parse_simple_args",
            side_effect=mock_parse_arguments_simple,
            return_value=(None, None),
        ),
        patch.object(
            target=controller,
            attribute="parse_known_args_and_warn",
            side_effect=mock_parse_known_args_and_warn_bound,
            return_value=None,
        ),
    ]

    if not session.settings.DEBUG_MODE:
        print_patch.start()
    patched_functions = [patcher.start() for patcher in patchers]

    yield patched_functions

    if not session.settings.DEBUG_MODE:
        print_patch.stop()
    for patcher in patchers:
        patcher.stop()


def get_argument_parser_from_command(
    controller,
    command_name: str,
) -> ArgumentParser:
    """Intercept the ArgumentParser instance from the command function.

    Parameters
    ----------
    controller: BaseController
        The CLI Controller instance.
    command_name: str
        Command name from `controller.CHOICES_COMMANDS`.

    Returns
    -------
    ArgumentParser: The ArgumentParser instance from the command function.
    """
    command_function: Callable = fetch_command_function(controller=controller, command_name=command_name)

    if not has_patchable_functions(command_function=command_function):
        raise AssertionError(
            f"Expected parse_simple_args or parse_known_args_and_warn in `call_{command_name}`."
        )

    with patch_controller_methods(controller=controller) as patched_functions:
        command_function([])

        call_count = 0
        for patched_function in patched_functions:
            call_count += patched_function.call_count
            if patched_function.call_count == 1:
                args, kwargs = patched_function.call_args
                argument_parser = kwargs.get("parser", args[0])

        if call_count != 1:
            raise AssertionError(
                f"Expected one call to parse_simple_args or parse_known_args_and_warn in `call_{command_name}`."
            )

    # pylint: disable=possibly-used-before-assignment
    return argument_parser


def construct_command_choice_map(argument_parser: ArgumentParser) -> dict:
    """Create a choice map from the ArgumentParser instance."""
    choice_map: dict = {}
    for action in argument_parser._actions:  # pylint: disable=protected-access
        if action.help == SUPPRESS:
            continue
        if len(action.option_strings) == 1:
            long_option = action.option_strings[0]
            short_option = ""
        elif len(action.option_strings) == 2:
            short_option = action.option_strings[0]
            long_option = action.option_strings[1]
        else:
            raise AttributeError(f"Invalid ArgumentParser configuration: {argument_parser}")

        if hasattr(action, "choices") and action.choices:
            choice_map[long_option] = {str(choice): {} for choice in action.choices}
        else:
            choice_map[long_option] = {}

        if short_option and long_option:
            choice_map[short_option] = long_option

    return choice_map


def build_choice_map_for_controller(controller) -> dict:
    """Construct a choice map for the given controller."""
    command_names = controller.CHOICES_COMMANDS
    controller_choice_map: dict = {cmd: {} for cmd in controller.controller_choices}

    for command_name in command_names:
        try:
            argument_parser = get_argument_parser_from_command(
                controller=controller,
                command_name=command_name,
            )
            controller_choice_map[command_name] = construct_command_choice_map(
                argument_parser=argument_parser
            )
        except Exception as error:
            if session.settings.DEBUG_MODE:
                raise Exception(
                    f"Error with command '{command_name}': {str(error)}"
                ) from error

    return controller_choice_map
