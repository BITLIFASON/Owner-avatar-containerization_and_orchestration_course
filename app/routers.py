"""FastAPI router module."""

from fastapi import APIRouter, HTTPException
from typing import Union

import crud, schemas

router = APIRouter()

@router.get('/health')
def health():
    print('health endpoint')


@router.post("/books")
async def add_book(book: Union[schemas.Book, None]) -> Union[str, None]:
    """
    Add book to library

    - Args:
        - book (Book): information about new book

    - Returns:
        - str | None: success message
    """

    if book:
        if book.id is not None:
            if crud.get_book_by_id(book.id):
                raise HTTPException(
                    status_code=404, detail="book with this id already exists"
                )
        crud.add_book_into_db(book)
        return "Success"
    else:
        raise HTTPException(status_code=404, detail="incorrect input data")


@router.get("/books/{id}")
async def get_book(id: int) -> Union[schemas.Book, None]:
    """
    View information about book

    - Args:
        - id (int | None): book id

    - Returns:
        - Book | None: information about book
    """

    book = crud.get_book_by_id(id)
    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail="book not found")


@router.put("/books/{id}")
async def update_book(
    id: int, book: Union[schemas.Book, None] = None
) -> Union[str, None]:
    """
    Update information about book

    - Args:
        - id (int): book id
        - book (Book): information about new book

    - Returns:
         - str | None: success message
    """

    if book.id != id:
        book.id = id
    if book:
        if crud.get_book_by_id(book.id) is None:
            raise HTTPException(
                status_code=404, detail="book with this id does not exist"
            )
    crud.update_book_by_id(book)
    return "Success"


@router.delete("/books/{id}")
async def delete_book(id: int) -> Union[str, None]:
    """
     Delete book from store

    - Args:
        - id (int): book id

    - Returns:
        - str | None: success message
    """

    if crud.get_book_by_id(id) is None:
        raise HTTPException(status_code=404, detail="book with this id does not exist")
    crud.delete_book_by_id(id)
    return "Success"
