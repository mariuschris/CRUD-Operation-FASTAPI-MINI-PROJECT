from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

# Creating Data model from in-buit Basemodel
class Book(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    publication_year: int
    genre: str

# initializing data memory
books_database = []
recent_id = 1

# Create a new book
@app.post("/book/", response_model=Book, status_code = status.HTTP_201_CREATED)
def create_book(book: Book):
    global recent_id
    book.id = recent_id
    books_database.append(book)
    recent_id += 1
    return book

# Get list of all books
@app.get("/book/", response_model=List[Book])
def get_books():
    return books_database

# get details of a specific book
@app.get("/book/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in books_database:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# update a book using ID
@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    for i, book in enumerate(books_database):
        if book.id == book_id:
            updated_book.id = book_id
            books_database[i] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

# Delete a book
@app.delete("/books/{book_id}", response_model=Book)
def delete_book(book_id: int):
    for i, book in enumerate(books_database):
        if book.id == book_id:
            books_database.pop(i)
            return "Book Deleted successfully"
    raise HTTPException(status_code=404, detail="Book not found")
