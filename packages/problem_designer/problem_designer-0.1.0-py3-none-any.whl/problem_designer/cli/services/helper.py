# import pyjson5 as json5   # ModuleNotFoundError when debugging with launch.json - change later
import json as json5
from pathlib import Path
from typing import Union

import pydantic

from problem_designer.typedef.spec import StrictDesignSpec


def parse_configuration(file_path: Union[str, Path], type_=StrictDesignSpec) -> StrictDesignSpec:
    """
    Parses a json file with JSON5 notation (comments allowed)
    Args:
        file_path: path to json file
        type_: Type which the file should be parsed to

    Returns: A valid problem design from the given json

    Raises:
        JSONDecodeError: When json is Invalid
        ValidationError: When pydantic schema does not match with json
    """
    with open(file_path) as handle:
        parsed = json5.load(handle)
        return pydantic.parse_obj_as(obj=parsed, type_=type_)
