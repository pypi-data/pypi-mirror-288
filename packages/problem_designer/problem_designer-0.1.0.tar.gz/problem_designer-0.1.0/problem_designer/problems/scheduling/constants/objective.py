from typing import Literal

from pydantic import BaseModel


class ObjectiveCMax(BaseModel):
    type: Literal["c-max"]


SupportedObjectives = ObjectiveCMax
