from fastapi import FastAPI, HTTPException, Depends
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
import models
from database import engine, Session_Local
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = Session_Local()
        yield db
    except:
        db.close()


class BookSchema(BaseModel):
    id: int = Field()
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=20)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=1, lt=101)


class BookCreateSchema(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=20)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=1, lt=101)


class FoodEnum(str, Enum):
    VEGETABLES = 'vegetables'
    FRUIT = 'fruit'


class ItemModel(BaseModel):
    name: str
    description: Optional[str] = None  # for less the python 3.10
    price: float
    tax: float | None = None  # for python >=3.10


@app.get("/")
async def root():
    return {"message": "Hello World"}


# path parameter
@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# enum url params
@app.get('/foods/{name}')
async def get_food_name(name: FoodEnum):
    return {"food name": name}


# query required parameter
@app.get('/foods/')
def get_query__required_parameter(number: int, test: str):
    return {test: number}


# query default parameter
@app.get('/foods/default/')
def get_query_default_parameter(number: int = 0, test: str = None):
    return {test: number}


# query optional parameter
@app.get('/foods/optional/')
def get_query_optional_parameter(test: str, number: Optional[int] = None):
    return {test: number}


@app.post('/items/')
async def create_item(item: ItemModel):
    item_dict = item.__dict__
    if item_dict['tax']:
        price_with_tax = item_dict['price'] + item_dict['tax']
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put('/items/{item_id}')
async def update_item(item_id: int, item: ItemModel, query: str | None = None):
    pass


# get book list from database
@app.get('/books/', response_model=list[BookSchema], tags=['Books'])
def get_books(db: Session = Depends(get_db)):
    return db.query(models.Books).all()


# add book into database
@app.post('/books/', tags=['Books'])
def create_book(book: BookCreateSchema, db: Session = Depends(get_db)):
    book_model = models.Books()
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating
    db.add(book_model)
    db.commit()
    return book


@app.get('/books/{book_id}/', tags=['Books'], response_model=BookSchema)
def retrieve_book(book_id: int, db: Session_Local = Depends(get_db)):
    book_obj = db.query(models.Books).filter(models.Books.id == book_id).first()
    if book_obj:
        return book_obj
    else:
        raise HTTPException(
            status_code=404,
            detail="Book does not found"
        )


@app.put('/books/{book_id}/', tags=['Books'])
def update_book(book_id: int, book: BookCreateSchema, db: Session_Local = Depends(get_db)):
    book_obj = db.query(models.Books).filter(models.Books.id == book_id).first()
    if book_obj:
        book_obj.title = book.title
        book_obj.author = book.author
        book_obj.description = book.description
        book_obj.rating = book.rating
        db.add(book_obj)
        db.commit()
        return book
    else:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )


@app.delete('/books/{book_id}/', tags=['Books'])
def delete_book(book_id: int, db: Session_Local = Depends(get_db)):
    book_obj = db.query(models.Books).filter(models.Books.id == book_id).first()
    if book_obj:
        db.query(models.Books).filter(models.Books.id == book_id).delete()
        db.commit()
        return {"detail": f"Book successfully deleted"}
    else:
        raise HTTPException(status_code=200, detail="Book not found")
