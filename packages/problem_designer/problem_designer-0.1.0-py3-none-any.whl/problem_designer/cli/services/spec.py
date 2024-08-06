import json
from pathlib import Path
from typing import Union

from problem_designer.cli.services.helper import parse_configuration
from problem_designer.cli.typedef import SpecNotFound
from problem_designer.plugin.manager import DesignSpecManager


class SpecService:
    def __init__(self):
        self._spec_manager = DesignSpecManager()
        self._specs = self._spec_manager.get_plugins()
        plugins = self._spec_manager.get_plugins()
        if plugins:
            self._spec_identifiers = sorted(plugins.keys())
        else:
            self._spec_identifiers = []

    def get_all_identifiers(self) -> list[str]:
        """
        Returns: All currently loaded identifiers

        """
        return self._spec_identifiers

    def parse_spec(self, id_: str, path: Union[Path, str]):
        if isinstance(path, str):
            path = Path(path)

        if self._specs is None:
            raise SpecNotFound("No specs are loaded!")

        if not self.is_valid_id(id_):
            raise SpecNotFound(f"Spec for identifier: {id_} not found! Registered: {self._spec_identifiers}")

        return parse_configuration(path, self._specs[id_].spec)

    def is_valid_id(self, id_: str) -> bool:
        """
        Check if the id is valid and corresponding plugin is loaded
        Args:
            id_: The identification of a plugin

        Returns: If the plugin is available
        """
        if id_ not in self.get_all_identifiers():
            return False
        return True

    def get_documentation(self, id_: str) -> tuple[str, str, str]:
        """
        Returns a summary of the document for any given problem design.
        Args:
            id_: The global id of the spec.

        Returns: The doc text for the problem design, the schema of the problem design and any examples

        Raises:
            SpecNotFound: If no specification for the given identifier is found
        """
        if self._specs is None:
            raise SpecNotFound("No specs are loaded!")

        if not self.is_valid_id(id_):
            raise SpecNotFound(f"Spec for identifier: {id_} not found! Registered: {self._spec_identifiers}")

        design_spec = self._specs[id_].spec
        return (
            str(design_spec.__doc__),
            json.dumps(design_spec.schema()),
            "Examples are not supported yet!",
        )
