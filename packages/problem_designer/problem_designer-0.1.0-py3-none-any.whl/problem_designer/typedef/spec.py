from pydantic import BaseModel


class StrictBaseModel(BaseModel):
    class Config:
        extra = "forbid"  # forbid any extra values in input json
        frozen = True  # should not be mutated


class MetaInfo(BaseModel):
    id: str
    category: str

    def get_global_identifier(self) -> str:
        return f"{self.category}_{self.id}"


class StrictDesignSpec(StrictBaseModel):
    meta: MetaInfo
