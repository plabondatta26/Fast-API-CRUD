from pydantic import BaseModel, Field


class BookCreateSchema(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=20)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=1, lt=101)


class BookSchema(BaseModel):
    id: int = Field()
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=20)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=1, lt=101)