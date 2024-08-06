import os

from pydantic_cli import SubParser

from problem_designer.cli.services.generator import GeneratorService
from problem_designer.cli.services.spec import SpecService
from problem_designer.typedef.plugin import GeneratorPlugin


def build_generator_runner(plugin: GeneratorPlugin):
    spec_service = SpecService()

    def generator_runner(options: plugin.options) -> int:
        # load spec
        spec = spec_service.parse_spec(plugin.meta.get_global_identifier(), options.spec_file)
        # generate
        plugin.generator(spec=spec, options=options).generate()
        return os.EX_OK

    return generator_runner


def build_generator_subparsers():
    generator_service = GeneratorService()
    return {
        f"gen_{id_}": SubParser(
            plugin.options,
            build_generator_runner(plugin),
            f"Generate data from problem specs for {id_}",
        )
        for id_, plugin in generator_service.get_generators().items()
    }
