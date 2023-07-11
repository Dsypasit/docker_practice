from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
import psycopg2
import os


class Book(BaseModel):
    title: str
    author: str
    publication_year: int


app = FastAPI()


def get_connection():
    conn = psycopg2.connect(
        host=os.environ.get("POSTGRES_URL"),
        database=os.environ.get("POSTGRES_DB"),
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
    )
    return conn


@app.get("/")
def read_root():
    return {"Hello": "World2"}

@app.get("/books/")
def create_book(book: Book):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    select * from books
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    if not results:
        raise HTTPException(status_code=404, detail="Book not found")
    book = [dict(zip(["id", "title", "author", "publication_year"], result)) for result in results]
    return book

@app.post("/books/")
def create_book(book: Book):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO books (title, author, publication_year)
    VALUES (%s, %s, %s)
    RETURNING id;
    """
    values = (book.title, book.author, book.publication_year)
    cursor.execute(query, values)
    book_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return {"id": book_id, **book.dict()}


@app.get("/books/{book_id}")
def read_book(book_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT * FROM books WHERE id = %s;
    """
    cursor.execute(query, (book_id,))
    result = cursor.fetchone()
    conn.close()
    if not result:
        raise HTTPException(status_code=404, detail="Book not found")
    book = dict(zip(["id", "title", "author", "publication_year"], result))
    return book


@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    UPDATE books
    SET title = %s, author = %s, publication_year = %s
    WHERE id = %s;
    """
    values = (book.title, book.author, book.publication_year, book_id)
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return {"id": book_id, **book.dict()}


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    DELETE FROM books WHERE id = %s;
    """
    cursor.execute(query, (book_id,))
    conn.commit()
    conn.close()
    return {"message": "Book deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)