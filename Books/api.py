from urllib.parse import quote_plus
from fastapi import Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Books import views
from Books.schema import BookCreate, BookUpdate, UserCreate, BorrowBook, ReturnBook
from config.db_config import SessionLocal
from pydantic import BaseModel

router = APIRouter()

# Dependency to get the database session

username = "postgres"
password = quote_plus("Password123#@!")
host = quote_plus("localhost")
port = quote_plus("5432")
database = quote_plus("library_ms")

# Construct the connection string
connection_string = f"postgresql://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(connection_string, echo=True)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


# Book Management


@router.post("/books/add/")
def add_book(book_details: BookCreate, db: Session = Depends(get_db)):
    try:
        book = views.create_book(book_details, db)
        return {
            "status": "success",
            "data": book,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = views.get_book_by_id(book_id, db)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {
        "status": "success",
        "data": book,
    }


@router.put("/books/{book_id}")
def update_book(book_id: int, new_data: BookUpdate, db: Session = Depends(get_db)):
    try:
        views.update_book(book_id, new_data.dict(), db)
        return {"status": "success", "message": "Book updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    try:
        views.delete_book(book_id, db)
        return {"status": "success", "message": "Book deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# User Management


@router.post("/users/add/")
def add_user(user_details: UserCreate, db: Session = Depends(get_db)):
    try:
        user = views.create_user(user_details, db)
        return {"status": "success", "data": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = views.get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "success", "data": user}

# Borrowed Books


@router.post("/borrow")
def borrow_book(borrow_details: BorrowBook, db: Session = Depends(get_db)):
    try:
        borrowed_book = views.borrow_book(borrow_details, db)
        return {"status": "success", "data": borrowed_book}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/return")
def return_book(return_details: ReturnBook, db: Session = Depends(get_db)):
    try:
        returned_book = views.return_book(return_details, db)
        return {"status": "success", "data": returned_book}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/borrowed-books")
def list_borrowed_books(db: Session = Depends(get_db)):
    borrowed_books = views.list_all_borrowed_books(db)
    return {"status": "success", "data": borrowed_books}
