import sys

from pydantic_cli import SubParser, run_sp_and_exit

from problem_designer.cli.cmd.documentation import (
    DocumentationCmdOptions,
    SchemaCmdOptions,
    documentation_runner,
    schema_runner,
)
from problem_designer.cli.cmd.generate import build_generator_subparsers
from problem_designer.cli.cmd.list import ListCmdOptions, list_runner
from problem_designer.cli.typedef import exception_to_exit_code


def to_subparser():
    commands = {
        "list": SubParser(ListCmdOptions, list_runner, "Lists all loaded available specs / generators"),
        "documentation": SubParser(
            DocumentationCmdOptions,
            documentation_runner,
            "Show documentation for a specific problem design",
        ),
        "schema": SubParser(
            SchemaCmdOptions,
            schema_runner,
            "Export json schema for a given spec",
        ),
    }
    commands.update(build_generator_subparsers())
    return commands


def custom_exception_handler(ex) -> int:
    sys.stderr.write(str(ex))
    exit_code = exception_to_exit_code.get(ex.__class__, 1)
    return exit_code


def run():
    run_sp_and_exit(
        to_subparser(),
        description="Generate scheduling problems from the given design",
        version="0.1.0",
        exception_handler=custom_exception_handler,
    )  # pragma: no cover


if __name__ == "__main__":
    run()
