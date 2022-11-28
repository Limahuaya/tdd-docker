# project/app/models/pydantic.py

from pydantic import validator
from pydantic import BaseModel
import validators

class SummaryPayloadSchema(BaseModel):
    url: str

    @validator('url')
    def username_length(cls, value):
        if type(validators.url(value)) is not bool:
            raise ValueError('Ingrese una url valida.')
        return value



class SummaryUpdatePayloadSchema(SummaryPayloadSchema):
    summary: str

        
class SummaryResponseSchema(SummaryPayloadSchema):
    id: int

class SummaryResponseUpdateSchema(SummaryUpdatePayloadSchema):
    id: int