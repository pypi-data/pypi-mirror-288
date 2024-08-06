from dataclasses import dataclass

from problem_designer.plugin.typedef import HookConstants, Plugin
from problem_designer.typedef.generator import Generator, GeneratorOptions
from problem_designer.typedef.spec import MetaInfo, StrictDesignSpec


@dataclass
class DesignSpecPlugin(Plugin):
    meta: MetaInfo
    spec: type[StrictDesignSpec]

    def get_id(self) -> str:
        return self.meta.get_global_identifier()


@dataclass
class GeneratorPlugin(Plugin):
    meta: MetaInfo
    generator: type[Generator]
    options: type[GeneratorOptions]

    def get_id(self) -> str:
        return self.meta.get_global_identifier()


DesignHookConstants = HookConstants("problem_designer.specs", "problem_designer.specs")


class DesignHookSpec:
    """
    Defines all hooks which are related to the problem schemata. Meaning they provide or interact with the
    problem design
    """

    @DesignHookConstants.spec
    def register_spec(
        self,
    ) -> list[tuple[MetaInfo, StrictDesignSpec]] | tuple[MetaInfo, StrictDesignSpec]:
        ...


GeneratorHookConstants = HookConstants("problem_designer.generators", "problem_designer.generators")


class GeneratorHookSpec:
    """
    Defines all hooks which are related to the problem schemata. Meaning they provide or interact with the
    problem design
    """

    @GeneratorHookConstants.spec
    def register_generator(
        self,
    ) -> list[tuple[MetaInfo, Generator]] | tuple[MetaInfo, Generator]:
        ...
