from pydantic import BaseModel
from typing import Union


class Book(BaseModel):
    id: Union[int, None] = None
    title: Union[str, None] = None
    author: Union[str, None] = None
    description: Union[str, None] = None
