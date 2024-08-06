import os
from io import StringIO

import rich
from pydantic import BaseModel
from rich.markdown import Markdown

from problem_designer.cli.services.spec import SpecService


class ListCmdOptions(BaseModel):
    pass


def list_runner(options: ListCmdOptions):
    service = SpecService()
    ids = service.get_all_identifiers()
    console = rich.console.Console()

    output = StringIO()
    output.write("# Loaded Modules\n")
    output.write(f"## Specs ({len(ids)})\n")
    for id_ in ids:
        output.write(f"- {id_}\n")
    console.print(Markdown(output.getvalue()))

    return os.EX_OK
