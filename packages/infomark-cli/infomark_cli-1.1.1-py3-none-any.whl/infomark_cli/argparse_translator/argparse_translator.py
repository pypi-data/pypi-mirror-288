"""Module for translating a function into an argparse program."""

import argparse
import inspect
import re
from copy import deepcopy
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Tuple,
    Type,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from infomark_core.app.model.field import InfomarkField
from pydantic import BaseModel
from typing_extensions import Annotated

from infomark_cli.argparse_translator.argparse_argument import (
    ArgparseArgumentGroupModel,
    ArgparseArgumentModel,
)
from infomark_cli.argparse_translator.utils import (
    get_argument_choices,
    get_argument_optional_choices,
    in_group,
    remove_argument,
    set_optional_choices,
)

# pylint: disable=protected-access

SEP = "__"

class ArgparseTranslator:
    """Class to translate a function into an argparse program."""

    def __init__(
        self,
        func: Callable,
        custom_argument_groups: Optional[List[ArgparseArgumentGroupModel]] = None,
        add_help: Optional[bool] = True,
    ):
        """
        Initialize the ArgparseTranslator.

        Args:
            func (Callable): The function to translate into an argparse program.
            custom_argument_groups (Optional[List[ArgparseArgumentGroupModel]], optional): Custom argument groups to add. Defaults to None.
            add_help (Optional[bool], optional): Whether to add the help argument. Defaults to True.
        """
        self.func = func
        self.signature = inspect.signature(func)
        self.type_hints = get_type_hints(func)
        self.provider_parameters: Dict[str, List[str]] = {}

        self._parser = argparse.ArgumentParser(
            prog=func.__name__,
            description=self._build_description(func.__doc__),  # type: ignore
            formatter_class=argparse.RawTextHelpFormatter,
            add_help=add_help,
        )
        self._required = self._parser.add_argument_group("required arguments")

        # Generate argparse arguments from function parameters
        if any(param in self.type_hints for param in self.signature.parameters):
            self._generate_argparse_arguments(self.signature.parameters)

        # Add custom argument groups if provided
        if custom_argument_groups:
            for group in custom_argument_groups:
                self.provider_parameters[group.name] = []
                argparse_group = self._parser.add_argument_group(group.name)
                for argument in group.arguments:
                    self._handle_argument_in_groups(argument, argparse_group)

    def _handle_argument_in_groups(self, argument, group):
        """Handle the argument and add it to the parser."""

        def _update_providers(
            input_string: str, new_provider: List[Optional[str]]
        ) -> str:
            """Update providers in the help string."""
            pattern = r"\(provider:\s*(.*?)\)"
            providers = re.findall(pattern, input_string)
            providers.extend(new_provider)
            input_string = re.sub(pattern, "", input_string).strip()
            return f"{input_string} (provider: {', '.join(providers)})"

        # Check if the argument is already in use, if not, add it
        if f"--{argument.name}" not in self._parser._option_string_actions:
            kwargs = argument.model_dump(exclude={"name"}, exclude_none=True)
            group.add_argument(f"--{argument.name}", **kwargs)
            if group.title in self.provider_parameters:
                self.provider_parameters[group.title].append(argument.name)
        else:
            kwargs = argument.model_dump(exclude={"name"}, exclude_none=True)
            model_choices = kwargs.get("choices", ()) or ()
            existing_choices = get_argument_choices(self._parser, argument.name)
            choices = tuple(set(existing_choices + model_choices))
            optional_choices = bool(existing_choices and not model_choices)

            if in_group(self._parser, argument.name, group_title="required arguments"):
                for action in self._required._group_actions:
                    if action.dest == argument.name and choices:
                        action.choices = choices
                        set_optional_choices(action, optional_choices)
                return

            if in_group(self._parser, argument.name, group_title="optional arguments"):
                for action in self._parser._actions:
                    if action.dest == argument.name:
                        if choices:
                            action.choices = choices
                            set_optional_choices(action, optional_choices)
                        if argument.name not in self.signature.parameters:
                            action.help = _update_providers(action.help or "", [group.title])
                return

            if not optional_choices:
                optional_choices = get_argument_optional_choices(self._parser, argument.name)

            groups_w_arg = remove_argument(self._parser, argument.name)
            groups_w_arg.append(group.title)
            if choices:
                kwargs["choices"] = choices
            kwargs["help"] = _update_providers(argument.help or "", groups_w_arg)
            action = self._parser.add_argument(f"--{argument.name}", **kwargs)
            set_optional_choices(action, optional_choices)

    @property
    def parser(self) -> argparse.ArgumentParser:
        """Get the argparse parser."""
        return deepcopy(self._parser)

    @staticmethod
    def _build_description(func_doc: str) -> str:
        """Build the description of the argparse program from the function docstring."""
        patterns = ["infomark\n        ======", "Parameters\n        ----------"]

        if func_doc:
            for pattern in patterns:
                if pattern in func_doc:
                    func_doc = func_doc[: func_doc.index(pattern)].strip()
                    break

        return func_doc

    @staticmethod
    def _param_is_default(param: inspect.Parameter) -> bool:
        """Return True if the parameter has a default value."""
        return param.default != inspect.Parameter.empty

    def _get_action_type(self, param: inspect.Parameter) -> str:
        """Return the argparse action type for the given parameter."""
        param_type = self.type_hints[param.name]
        type_origin = get_origin(param_type)

        if param_type == bool or (
            type_origin is Union and bool in get_args(param_type)
        ):
            return "store_true"
        return "store"

    def _get_type_and_choices(
        self, param: inspect.Parameter
    ) -> Tuple[Type[Any], Tuple[Any, ...]]:
        """Return the type and choices for the given parameter."""
        param_type = self.type_hints[param.name]
        type_origin = get_origin(param_type)

        choices: tuple[Any, ...] = ()

        if type_origin is Literal:
            choices = get_args(param_type)
            param_type = type(choices[0])  # type: ignore

        if type_origin is list:
            param_type = get_args(param_type)[0]
            if get_origin(param_type) is Literal:
                choices = get_args(param_type)
                param_type = type(choices[0])  # type: ignore

        if type_origin is Union:
            union_args = get_args(param_type)
            if str in union_args:
                param_type = str

            if type(None) in get_args(param_type):
                args = [arg for arg in get_args(param_type) if arg != type(None)]
                if len(args) > 1:
                    raise ValueError("Union with NoneType should have only one type left")
                param_type = args[0]
                if get_origin(param_type) is Literal:
                    choices = get_args(param_type)
                    param_type = type(choices[0])  # type: ignore

        choices = self._get_argument_custom_choices(param) or choices  # type: ignore

        return param_type, choices

    @staticmethod
    def _split_annotation(
        base_annotation: Type[Any], custom_annotation_type: Type
    ) -> Tuple[Type[Any], List[Any]]:
        """Find the base annotation and the custom annotations, namely the InfomarkField."""
        if get_origin(base_annotation) is not Annotated:
            return base_annotation, []
        base_annotation, *maybe_custom_annotations = get_args(base_annotation)
        return base_annotation, [
            annotation
            for annotation in maybe_custom_annotations
            if isinstance(annotation, custom_annotation_type)
        ]

    @classmethod
    def _get_argument_custom_help(cls, param: inspect.Parameter) -> Optional[str]:
        """Return the help annotation for the given parameter."""
        base_annotation = param.annotation
        _, custom_annotations = cls._split_annotation(base_annotation, InfomarkField)
        help_annotation = (
            custom_annotations[0].description if custom_annotations else None
        )
        return help_annotation

    @classmethod
    def _get_argument_custom_choices(cls, param: inspect.Parameter) -> Optional[str]:
        """Return the choices annotation for the given parameter."""
        base_annotation = param.annotation
        _, custom_annotations = cls._split_annotation(base_annotation, InfomarkField)
        choices_annotation = (
            custom_annotations[0].choices if custom_annotations else None
        )
        return choices_annotation

    def _get_nargs(self, param: inspect.Parameter) -> Optional[str]:
        """Return the nargs annotation for the given parameter."""
        param_type = self.type_hints[param.name]
        origin = get_origin(param_type)

        if origin is list:
            return "+"

        if origin is Union and any(
            get_origin(arg) is list for arg in get_args(param_type)
        ):
            return "+"

        return None

    def _generate_argparse_arguments(self, parameters) -> None:
        """Generate the argparse arguments from the function parameters."""
        for param in parameters.values():
            if param.name == "kwargs":
                continue

            param_type, choices = self._get_type_and_choices(param)

            if inspect.isclass(param_type) and issubclass(param_type, BaseModel):
                type_hints = get_type_hints(param_type)
                type_hints.pop("kwargs", None)

                for name, sub_param in type_hints.items():
                    if name in self.signature.parameters:
                        continue

                    self._handle_argument_in_groups(
                        ArgparseArgumentModel(
                            name=name,
                            type_=sub_param,
                            help=self._get_argument_custom_help(param),
                            choices=self._get_argument_custom_choices(param),
                            default=self._get_default_value(sub_param),
                            nargs=self._get_nargs(param),
                        ),
                        self._required,
                    )
                continue

            self._handle_argument_in_groups(
                ArgparseArgumentModel(
                    name=param.name,
                    type_=param_type,
                    help=self._get_argument_custom_help(param),
                    choices=self._get_argument_custom_choices(param),
                    default=self._get_default_value(param_type),
                    nargs=self._get_nargs(param),
                ),
                self._required if self._param_is_default(param) else self._parser,
            )

    def _get_default_value(self, param_type: Type[Any]) -> Any:
        """Return the default value for the given parameter type."""
        if param_type in [bool, "bool"]:
            return False
        return None
