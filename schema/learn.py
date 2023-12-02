from typing import Optional

from pydantic import BaseModel


class ItemModel(BaseModel):
    name: str
    description: Optional[str] = None  # for less the python 3.10
    price: float
    tax: float | None = None  # for python >=3.10
