import pydantic
import typing


class NewBook(pydantic.BaseModel):
    title : str
    author : str
    published_year : int


class book_reviews(pydantic.BaseModel):
    text_review : typing.Optional[str]
    rating : float

class update_book(pydantic.BaseModel):
    title : str
    author : str
    published_year : int

class review_details(pydantic.BaseModel):
    text_review : typing.Optional[str]
    rating : float

class address(pydantic.BaseModel):
    name: str
    latitude: float
    longitude: float