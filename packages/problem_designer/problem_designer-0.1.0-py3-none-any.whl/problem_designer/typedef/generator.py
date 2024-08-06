from pathlib import Path

from pydantic import BaseModel, Field


class GeneratorOptions(BaseModel):
    spec_file: Path = Field(description="Path of input design spec", cli=("-f", "--file"))


class Generator:
    def __init__(self, spec, options):
        pass

    def generate(self):
        raise NotImplementedError
