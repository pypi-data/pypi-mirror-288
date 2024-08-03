"""Platform Management Controller."""

import os
from functools import partial, update_wrapper
from types import MethodType
from typing import Dict, List, Optional

import pandas as pd
from infomark import ifm
from infomark_charting.core.infomark_figure import InfomarkFigure
from infomark_cli.argparse_translator.argparse_class_processor import (
    ArgparseClassProcessor,
)
from infomark_cli.config.menu_text import MenuText
from infomark_cli.controllers.base_controller import BaseController
from infomark_cli.controllers.utils import export_data, print_rich_table
from infomark_cli.session import Session
from infomark_core.app.model.ifm_object import IFMObject

session = Session()


class DummyTranslation:
    """Dummy Translation class for testing purposes."""

    def __init__(self):
        """Initialize Dummy Translation."""
        self.paths = {}
        self.translators = {}


class PlatformControllerBase(BaseController):
    """Base class for managing platform commands and controllers."""

    CHOICES_GENERATION = True

    def __init__(
        self,
        name: str,
        parent_path: List[str],
        platform_target: Optional[type] = None,
        queue: Optional[List[str]] = None,
        translators: Optional[Dict] = None,
    ):
        """Initialize the Platform Controller Base."""
        self.PATH = f"/{'/'.join(parent_path)}/{name}/" if parent_path else f"/{name}/"
        super().__init__(queue)
        self._name = name

        if not (platform_target or translators):
            raise ValueError("Either platform_target or translators must be provided.")

        self._translated_target = (
            ArgparseClassProcessor(
                target_class=platform_target, reference=ifm.reference["paths"]
            )
            if platform_target
            else DummyTranslation()
        )
        self.translators = (
            translators
            if translators is not None
            else getattr(self._translated_target, "translators", {})
        )
        self.paths = getattr(self._translated_target, "paths", {})

        if self.translators:
            self._link_ifm_object_to_data_processing_commands()
            self._generate_commands()
            self._generate_sub_controllers()
            self.update_completer(self.choices_default)

    def _link_ifm_object_to_data_processing_commands(self):
        """Link data processing commands to IFMObject registry."""
        for _, trl in self.translators.items():
            for action in trl._parser._actions:
                if action.dest == "data":
                    action.choices = [
                        f"IFM{str(i)}"
                        for i in range(len(session.ifm_object_registry.ifm_objects))
                    ] + [
                        ifm_object.extra.get("register_key", "")
                        for ifm_object in session.ifm_object_registry.ifm_objects
                        if "register_key" in ifm_object.extra
                    ]
                    action.type = str
                    action.nargs = None

    def _intersect_data_processing_commands(self, ns_parser):
        """Convert data command strings to IFMObject instances."""
        if hasattr(ns_parser, "data"):
            if "IFM" in ns_parser.data:
                ns_parser.data = int(ns_parser.data.replace("IFM", ""))

            if (ns_parser.data in range(len(session.ifm_object_registry.ifm_objects))) or (
                ns_parser.data in session.ifm_object_registry.ifm_object_keys
            ):
                ifm_object = session.ifm_object_registry.get(ns_parser.data)
                if isinstance(ifm_object, IFMObject):
                    setattr(ns_parser, "data", ifm_object.results)

        return ns_parser

    def _generate_sub_controllers(self):
        """Generate sub-controllers based on paths."""
        for path, value in self.paths.items():
            if value == "path":
                continue

            sub_menu_translators = {}
            choices_commands = []

            for translator_name, translator in self.translators.items():
                if f"{self._name}_{path}" in translator_name:
                    new_name = translator_name.replace(f"{self._name}_{path}_", "")
                    sub_menu_translators[new_name] = translator
                    choices_commands.append(new_name)

                    if translator_name in self.CHOICES_COMMANDS:
                        self.CHOICES_COMMANDS.remove(translator_name)

            class_name = f"{self._name.capitalize()}{path.capitalize()}Controller"
            SubController = type(
                class_name,
                (PlatformControllerBase,),
                {
                    "CHOICES_GENERATION": True,
                    "CHOICES_COMMANDS": choices_commands,
                },
            )

            self._generate_controller_call(
                controller=SubController,
                name=path,
                parent_path=self.path,
                translators=sub_menu_translators,
            )

    def _generate_commands(self):
        """Generate command methods for each translator."""
        for name, translator in self.translators.items():
            new_name = name.replace(f"{self._name}_", "")
            self._generate_command_call(name=new_name, translator=translator)

    def _generate_command_call(self, name, translator):
        """Create a command method to handle the translator."""
        def method(self, other_args: List[str], translator=translator):
            """Execute the command associated with the translator."""
            parser = translator.parser

            if ns_parser := self.parse_known_args_and_warn(
                parser=parser,
                other_args=other_args,
                export_allowed="raw_data_and_figures",
            ):
                try:
                    ns_parser = self._intersect_data_processing_commands(ns_parser)
                    export = hasattr(ns_parser, "export") and ns_parser.export
                    store_ifm_object = (
                        hasattr(ns_parser, "register_ifm_object")
                        and ns_parser.register_ifm_object
                    )

                    ifm_object = translator.execute_func(parsed_args=ns_parser)
                    df: pd.DataFrame = pd.DataFrame()
                    fig: Optional[InfomarkFigure] = None
                    title = f"{self.PATH}{translator.func.__name__}"

                    if ifm_object:
                        if isinstance(ifm_object, IFMObject):
                            if session.max_ifm_objects_exceeded() and ifm_object.results and store_ifm_object:
                                session.ifm_object_registry.remove()
                                session.console.print(
                                    "[yellow]Maximum number of IFMObjects reached. The oldest entry was removed.[yellow]"
                                )

                            ifm_object.extra["command"] = f"{title} {' '.join(other_args)}"
                            if hasattr(ns_parser, "register_key") and ns_parser.register_key:
                                if ns_parser.register_key not in session.ifm_object_registry.ifm_object_keys:
                                    ifm_object.extra["register_key"] = str(ns_parser.register_key)
                                else:
                                    session.console.print(
                                        f"[yellow]Key `{ns_parser.register_key}` already exists in the registry."
                                        "The `IFMObject` was kept without the key.[/yellow]"
                                    )

                            if store_ifm_object:
                                register_result = session.ifm_object_registry.register(ifm_object)
                                self._link_ifm_object_to_data_processing_commands()
                                self.update_completer(self.choices_default)

                                if session.settings.SHOW_MSG_IFMOBJECT_REGISTRY and register_result:
                                    session.console.print("Added `IFMObject` to cached results.")

                            df = ifm_object.to_dataframe()

                            if hasattr(ns_parser, "chart") and ns_parser.chart:
                                fig = ifm_object.chart.fig if ifm_object.chart else None
                                if not export:
                                    ifm_object.show()
                            else:
                                if isinstance(df.columns, pd.RangeIndex):
                                    df.columns = [str(i) for i in df.columns]

                                print_rich_table(
                                    df=df, show_index=True, title=title, export=export
                                )

                        elif isinstance(ifm_object, dict):
                            df = pd.DataFrame.from_dict(ifm_object, orient="columns")
                            print_rich_table(
                                df=df, show_index=True, title=title, export=export
                            )

                        elif not isinstance(ifm_object, IFMObject):
                            session.console.print(ifm_object)

                    if export and not df.empty:
                        sheet_name = getattr(ns_parser, "sheet_name", None)
                        if sheet_name and isinstance(sheet_name, list):
                            sheet_name = sheet_name[0]

                        export_data(
                            export_type=",".join(ns_parser.export),
                            dir_path=os.path.dirname(os.path.abspath(__file__)),
                            func_name=translator.func.__name__,
                            df=df,
                            sheet_name=sheet_name,
                            figure=fig,
                        )
                    elif export and df.empty:
                        session.console.print("[yellow]No data to export.[/yellow]")

                except Exception as e:
                    session.console.print(f"[red]{e}[/]\n")
                    return

        bound_method = MethodType(method, self)
        bound_method = update_wrapper(
            partial(bound_method, translator=translator), method
        )
        setattr(self, f"call_{name}", bound_method)

    def _generate_controller_call(self, controller, name, parent_path, translators):
        """Create a method to initialize and call a sub-controller."""
        def method(self, _, controller, name, parent_path, translators):
            """Initialize and call the specified sub-controller."""
            self.queue = self.load_class(
                class_ins=controller,
                name=name,
                parent_path=parent_path,
                translators=translators,
                queue=self.queue,
            )

        bound_method = MethodType(method, self)
        bound_method = update_wrapper(
            partial(
                bound_method,
                name=name,
                parent_path=parent_path,
                translators=translators,
                controller=controller,
            ),
            method,
        )
        setattr(self, f"call_{name}", bound_method)

    def _get_command_description(self, command: str) -> str:
        """Retrieve a description for a given command."""
        command_description = (
            ifm.reference["paths"]
            .get(f"{self.PATH}{command}", {})
            .get("description", "")
        )

        if not command_description:
            trl = self.translators.get(
                f"{self._name}_{command}"
            ) or self.translators.get(command)
            if trl and hasattr(trl, "parser"):
                command_description = trl.parser.description

        return command_description.split(".")[0].lower()

    def _get_menu_description(self, menu: str) -> str:
        """Retrieve description for a menu."""
        def _get_sub_menu_commands():
            """List commands in a sub-menu."""
            sub_path = f"{self.PATH[1:].replace('/','_')}{menu}"
            commands = [
                trl.replace(f"{sub_path}_", "")
                for trl in self.translators
                if sub_path in trl
            ]
            return commands

        menu_description = (
            ifm.reference["routers"]
            .get(f"{self.PATH}{menu}", {})
            .get("description", "")
        ) or ""

        if menu_description:
            return menu_description.split(".")[0].lower()

        return ", ".join(_get_sub_menu_commands())

    def print_help(self):
        """Display help text with menu and command descriptions."""
        mt = MenuText(self.PATH)

        if self.CHOICES_MENUS:
            for menu in self.CHOICES_MENUS:
                description = self._get_menu_description(menu)
                mt.add_menu(name=menu, description=description)

            if self.CHOICES_COMMANDS:
                mt.add_raw("\n")

        if self.CHOICES_COMMANDS:
            for command in self.CHOICES_COMMANDS:
                command_description = self._get_command_description(command)
                mt.add_cmd(
                    name=command.replace(f"{self._name}_", ""),
                    description=command_description,
                )

        if session.ifm_object_registry.ifm_objects:
            mt.add_info("\nCached Results")
            for key, value in list(session.ifm_object_registry.all.items())[
                : session.settings.N_TO_DISPLAY_IFM_OBJECT_REGISTRY
            ]:
                mt.add_raw(
                    f"[yellow]IFM{key}[/yellow]: {value['command']}",
                    left_spacing=True,
                )

        session.console.print(text=mt.menu_text, menu=self.PATH)

        if mt.warnings:
            session.console.print("")
            for w in mt.warnings:
                w_str = str(w).replace("{", "").replace("}", "").replace("'", "")
                session.console.print(f"[yellow]{w_str}[/yellow]")
            session.console.print("")
