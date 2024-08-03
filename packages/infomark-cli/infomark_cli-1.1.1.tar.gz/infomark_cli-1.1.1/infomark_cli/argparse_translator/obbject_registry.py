"""Registry for InfomarkObjects."""

import json
from typing import Dict, List, Optional, Union

from infomark_core.app.model.infomark_object import InfomarkObject


class Registry:
    """Registry for InfomarkObjects."""

    def __init__(self):
        """Initialize the registry."""
        self._infomark_objects: List[InfomarkObject] = []

    @staticmethod
    def _contains_infomark_object(uuid: str, infomark_objects: List[InfomarkObject]) -> bool:
        """Check if an InfomarkObject with uuid is in the registry."""
        return any(obj.id == uuid for obj in infomark_objects)

    def register(self, obj: InfomarkObject) -> bool:
        """Add an InfomarkObject instance to the registry."""
        if (
            isinstance(obj, InfomarkObject)
            and not self._contains_infomark_object(obj.id, self._infomark_objects)
            and obj.results
        ):
            self._infomark_objects.append(obj)
            return True
        return False

    def get(self, arg: Union[int, str]) -> Optional[InfomarkObject]:
        """Return the InfomarkObject with index or key."""
        if isinstance(arg, int):
            return self._get_by_index(arg)
        if isinstance(arg, str):
            return self._get_by_key(arg)

        raise ValueError("Couldn't get the `InfomarkObject` with the provided argument.")

    def _get_by_key(self, key: str) -> Optional[InfomarkObject]:
        """Return the InfomarkObject with key."""
        for obj in self._infomark_objects:
            if obj.extra.get("register_key", "") == key:
                return obj
        return None

    def _get_by_index(self, idx: int) -> Optional[InfomarkObject]:
        """Return the InfomarkObject at index idx."""
        # the list should work as a stack
        # i.e., the last element needs to be accessed by idx=0 and so on
        reversed_list = list(reversed(self._infomark_objects))

        # check if the index is out of bounds
        if idx >= len(reversed_list):
            return None

        return reversed_list[idx]

    def remove(self, idx: int = -1):
        """Remove the InfomarkObject at index idx, default is the last element."""
        # the list should work as a stack
        # i.e., the last element needs to be accessed by idx=0 and so on
        reversed_list = list(reversed(self._infomark_objects))
        del reversed_list[idx]
        self._infomark_objects = list(reversed(reversed_list))

    @property
    def all(self) -> Dict[int, Dict]:
        """Return all InfomarkObjects in the registry."""

        def _handle_standard_params(obj: InfomarkObject) -> str:
            """Handle standard params for InfomarkObjects."""
            standard_params_json = ""
            std_params = getattr(
                obj, "_standard_params", {}
            )  # pylint: disable=protected-access
            if std_params:
                standard_params = {
                    k: str(v)[:30] for k, v in std_params.items() if v and k != "data"
                }
                standard_params_json = json.dumps(standard_params)

            return standard_params_json

        def _handle_data_repr(obj: InfomarkObject) -> str:
            """Handle data representation for InfomarkObjects."""
            data_repr = ""
            if hasattr(obj, "results") and obj.results:
                data_schema = (
                    obj.results[0].model_json_schema()
                    if obj.results and isinstance(obj.results, list)
                    else ""
                )
                if data_schema and "title" in data_schema:
                    data_repr = f"{data_schema['title']}"
                if data_schema and "description" in data_schema:
                    data_repr += f" - {data_schema['description'].split('.')[0]}"

            return data_repr

        infomark_objects = {}
        for i, obj in enumerate(list(reversed(self._infomark_objects))):
            infomark_objects[i] = {
                "route": obj._route,  # pylint: disable=protected-access
                "provider": obj.provider,
                "standard params": _handle_standard_params(obj),
                "data": _handle_data_repr(obj),
                "command": obj.extra.get("command", ""),
                "key": obj.extra.get("register_key", ""),
            }

        return infomark_objects

    @property
    def infomark_objects(self) -> List[InfomarkObject]:
        """Return all InfomarkObjects in the registry."""
        return self._infomark_objects

    @property
    def infomark_object_keys(self) -> List[str]:
        """Return all InfomarkObject keys in the registry."""
        return [
            obj.extra["register_key"]
            for obj in self._infomark_objects
            if "register_key" in obj.extra
        ]
