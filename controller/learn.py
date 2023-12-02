from typing import Optional

from fastapi import APIRouter

from schema.learn import ItemModel
from utils.enum import FoodEnum

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}


# path parameter
@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# enum url params
@router.get('/foods/{name}')
async def get_food_name(name: FoodEnum):
    return {"food name": name}


# query required parameter
@router.get('/foods/')
def get_query__required_parameter(number: int, test: str):
    return {test: number}


# query default parameter
@router.get('/foods/default/')
def get_query_default_parameter(number: int = 0, test: str = None):
    return {test: number}


# query optional parameter
@router.get('/foods/optional/')
def get_query_optional_parameter(test: str, number: Optional[int] = None):
    return {test: number}


@router.post('/items/')
async def create_item(item: ItemModel):
    item_dict = item.__dict__
    if item_dict['tax']:
        price_with_tax = item_dict['price'] + item_dict['tax']
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@router.put('/items/{item_id}')
async def update_item(item_id: int, item: ItemModel, query: str | None = None):
    pass
