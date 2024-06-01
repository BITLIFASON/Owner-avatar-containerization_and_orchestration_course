"""Data access wrappers."""

import os
from typing import Union
import psycopg2
from psycopg2.extras import RealDictCursor

import schemas


DATABASE_URL = f"postgres://{os.getenv('POSTGRES_USER_APP','')}:{os.getenv('POSTGRES_PASSWORD_APP','')}@{os.getenv('POSTGRES_HOST','')}/{os.getenv('POSTGRES_DB_APP','')}"

def create_db():
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS book(
            id SERIAL PRIMARY KEY,
            title VARCHAR(50),
            author VARCHAR(20),
            description VARCHAR(500))"""
    )

    connection.commit()
    connection.close()


def add_book_into_db(book: schemas.Book):
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO book (title, author, description) VALUES (%s, %s, %s) RETURNING id",
        (book.title, book.author, book.description),
    )
    book.id = cursor.fetchone()[0]

    connection.commit()
    connection.close()


def get_book_by_id(id: int) -> Union[schemas.Book, None]:
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT * FROM book WHERE id = %s", (id,))
    result = cursor.fetchone()

    connection.close()

    if result:
        return schemas.Book(**result)
    else:
        return None


def update_book_by_id(book: schemas.Book):
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE book SET title=%s, author=%s, description=%s WHERE id=%s",
        (book.title, book.author, book.description, book.id),
    )

    connection.commit()
    connection.close()


def delete_book_by_id(id: int):
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM book WHERE id=%s", (id,))

    connection.commit()
    connection.close()
