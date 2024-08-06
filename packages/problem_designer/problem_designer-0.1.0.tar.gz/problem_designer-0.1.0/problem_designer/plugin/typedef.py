from dataclasses import dataclass
from types import ModuleType

import pluggy


class Plugin:
    def get_id(self) -> str:
        raise NotImplementedError


@dataclass
class HookConstants:
    """
    Defines constants which are used to access hooks. Including the entrypoint group which can be defined via
    pyproject.toml or similar. See the pluggy framework for details.
    """

    namespace: str
    entrypoint_group: str

    def __post_init__(self):
        self.spec = pluggy.HookspecMarker(self.namespace)
        self.impl = pluggy.HookimplMarker(self.namespace)


HookContainer = ModuleType | type
