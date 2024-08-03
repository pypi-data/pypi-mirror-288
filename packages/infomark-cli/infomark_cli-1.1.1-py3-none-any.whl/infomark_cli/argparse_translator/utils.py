"""Utilities for the argparse_translator module."""

from argparse import Action, ArgumentParser
from typing import List, Optional, Tuple


def is_argument_in_group(parser: ArgumentParser, arg_name: str, group_title: str) -> bool:
    """Determine if an argument is part of a specified group in an ArgumentParser."""
    for group in parser._action_groups:  # pylint: disable=protected-access
        if group.title == group_title:
            for action in group._group_actions:  # pylint: disable=protected-access
                options = action.option_strings
                if (options and options[0] == arg_name) or action.dest == arg_name:
                    return True
    return False


def delete_argument(parser: ArgumentParser, arg_name: str) -> List[Optional[str]]:
    """Remove a specific argument from an ArgumentParser and return affected groups."""
    affected_groups = []

    # Remove the argument from the parser itself
    for action in parser._actions:  # pylint: disable=protected-access
        options = action.option_strings
        if (options and options[0] == arg_name) or action.dest == arg_name:
            parser._remove_action(action)  # pylint: disable=protected-access
            break

    # Remove the argument from all associated groups
    for group in parser._action_groups:  # pylint: disable=protected-access
        for action in group._group_actions:  # pylint: disable=protected-access
            options = action.option_strings
            if (options and options[0] == arg_name) or action.dest == arg_name:
                group._group_actions.remove(action)  # pylint: disable=protected-access
                affected_groups.append(group.title)

    # Clean up the _option_string_actions dictionary
    parser._option_string_actions.pop(f"--{arg_name}", None)  # pylint: disable=protected-access

    return affected_groups


def retrieve_argument_choices(parser: ArgumentParser, arg_name: str) -> Tuple:
    """Fetch the choices available for a specific argument in an ArgumentParser."""
    for action in parser._actions:  # pylint: disable=protected-access
        options = action.option_strings
        if (options and options[0] == arg_name) or action.dest == arg_name:
            return tuple(action.choices or ())
    return ()


def get_optional_choices_for_argument(parser: ArgumentParser, arg_name: str) -> bool:
    """Retrieve the optional_choices attribute of an argument, if present."""
    for action in parser._actions:  # pylint: disable=protected-access
        options = action.option_strings
        if (
            (options and options[0] == arg_name)
            or action.dest == arg_name
            and hasattr(action, "optional_choices")
        ):
            return (
                action.optional_choices  # type: ignore[attr-defined] # this is a custom attribute
            )
    return False


def define_optional_choices(action: Action, optional_choices: bool):
    """Assign the optional_choices attribute to an action."""
    if not hasattr(action, "optional_choices") and optional_choices:
        setattr(action, "optional_choices", optional_choices)
