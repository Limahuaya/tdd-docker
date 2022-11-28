# project/app/models/pydantic.py

import validators
from pydantic import BaseModel, validator


class SummaryPayloadSchema(BaseModel):
    url: str

    @validator("url")
    def username_length(cls, value):
        if type(validators.url(value)) is not bool:
            raise ValueError("Ingrese una url valida.")
        return value


class SummaryUpdatePayloadSchema(SummaryPayloadSchema):
    summary: str


class SummaryResponseSchema(SummaryPayloadSchema):
    id: int


class SummaryResponseUpdateSchema(SummaryUpdatePayloadSchema):
    id: int
