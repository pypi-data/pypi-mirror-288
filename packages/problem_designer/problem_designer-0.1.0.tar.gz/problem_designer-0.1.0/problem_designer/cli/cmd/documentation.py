import os
from pathlib import Path

import rich
from pydantic import BaseModel
from rich.markdown import Markdown

from problem_designer.cli.services.spec import SpecService
from problem_designer.cli.typedef import SpecNotFound


class DocumentationCmdOptions(BaseModel):
    id: str


class SchemaCmdOptions(BaseModel):
    id: str
    output_path: Path


def documentation_runner(options: DocumentationCmdOptions):
    service = SpecService()

    if not service.is_valid_id(options.id):
        raise SpecNotFound(f"Id {options.id} was not found. Available: {service.get_all_identifiers()}")

    text, schema, examples = service.get_documentation(options.id)

    console = rich.console.Console()
    console.print(Markdown(f"# Documentation (id: {options.id})"))
    console.print(Markdown("## Description"))
    console.print(Markdown(text))
    console.print(Markdown("## Schema"))
    console.print(schema)
    console.print(Markdown("## Examples"))
    console.print(examples)

    return os.EX_OK


def schema_runner(options: SchemaCmdOptions):
    service = SpecService()

    if not service.is_valid_id(options.id):
        raise SpecNotFound(f"Id {options.id} was not found. Available: {service.get_all_identifiers()}")

    _, schema, _ = service.get_documentation(options.id)

    console = rich.console.Console()
    console.print_json(schema)
    options.output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(options.output_path, "w") as f:
        f.write(schema)
    console.print(f"Wrote schema to {options.output_path}")

    return os.EX_OK
