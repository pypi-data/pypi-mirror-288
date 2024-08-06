from problem_designer.plugin.manager import GeneratorManager
from problem_designer.typedef.plugin import GeneratorPlugin


class GeneratorService:
    def __init__(self):
        self._generator_manager = GeneratorManager()
        self._generators = self._generator_manager.get_plugins()
        plugins = self._generator_manager.get_plugins()
        self._generators = plugins
        if plugins:
            self._identifiers = sorted(plugins.keys())
        else:
            self._identifiers = []

    def get_all_identifiers(self) -> list[str]:
        return self._identifiers

    def get_generators(self) -> dict[str, GeneratorPlugin]:
        return self._generators
