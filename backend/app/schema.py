from datetime import date
from typing import Optional, TypeVar, Generic, List

from fastapi import HTTPException
from pydantic import BaseModel, validator
from pydantic.generics import GenericModel

from models.person import Sex

T = TypeVar('T')


class PersonCreate(BaseModel):
    name: str
    sex: Sex
    birth_date: date
    birth_place: str
    country: str

    # sex validation
    @validator("sex")
    def sex_validation(cls, v):
        if hasattr(Sex, v) is False:
            raise HTTPException(status_code=400, detail="Invalid input")
        return v


class ResponseSchema(BaseModel):
    detail: str
    result: Optional[T] = None


class PageResponse(GenericModel, Generic[T]):
    """ The Response for Pagination Query """

    page_number: int
    page_size: int
    total_pages: int
    total_records: int
    content: List[T]
