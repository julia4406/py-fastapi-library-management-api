from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class AuthorCreateSchema(BaseModel):
    name: str
    bio:str

    model_config = {"from_attributes": True}


class BookCreateSchema(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int

    model_config = {"from_attributes": True}


class BookDetailSchema(BookCreateSchema):
    id: int


class AuthorDetailSchema(AuthorCreateSchema):
    id: int
    books: Optional[list["BookDetailSchema"]] = None


class AuthorUpdateSchema(BaseModel):
    name: Optional[str]
    bio: Optional[str]

    model_config = {"from_attributes": True}


class AuthorCreateResponseSchema(AuthorCreateSchema):
    id: int
