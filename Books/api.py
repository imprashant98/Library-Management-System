from urllib.parse import quote_plus
from fastapi import Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Books import views
from Books.schema import BookDetailsBase, BookDetailsCreate, BookDetailsUpdate, BookBase, BookCreate, BookUpdate, UserBase, UserCreate, UserUpdate, BorrowBook, ReturnBook, BorrowedBookBase, BorrowedBookCreate, BorrowedBookUpdate, BorrowedBookResponse
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
def create_book(book_details: BookCreate, db: Session = Depends(get_db)):
    return views.create_book(book_details, db)


@router.get("/books/{book_id}")
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = views.get_book_by_id(book_id, db)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/books/{book_id}")
def update_book(book_id: int, new_data: dict, db: Session = Depends(get_db)):
    book = views.update_book(book_id, new_data, db)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    success = views.delete_book(book_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"detail": "Book deleted successfully"}
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


@router.put("/users/{user_id}")
def update_user(user_id: int, user_details: dict, db: Session = Depends(get_db)):
    user = views.update_user(user_id, user_details, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "success", "data": user}


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = views.delete_user(user_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}

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

# Books Details


@router.post("/books/{book_id}/details")
def create_book_details(book_id: int, book_details: BookDetailsCreate, db: Session = Depends(get_db)):
    try:
        existing_book = views.get_book_by_id(book_id, db)

        if existing_book is None:
            raise HTTPException(status_code=404, detail="Book not found")

        book = views.create_book_details(book_id, book_details, db)
        return {"status": "success", "data": book}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/books/{book_id}/details")
def update_book_details(book_id: int, book_details: BookDetailsUpdate, db: Session = Depends(get_db)):
    try:
        existing_book = views.get_book_by_id(book_id, db)

        if existing_book is None:
            raise HTTPException(status_code=404, detail="Book not found")

        if existing_book.book_details is None:
            raise HTTPException(
                status_code=404, detail="Book details not found")

        book = views.update_book_details(book_id, book_details, db)
        return {"status": "success", "data": book}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/books/{book_id}/details")
def read_book_details(book_id: int, db: Session = Depends(get_db)):
    try:
        existing_book = views.get_book_by_id(book_id, db)

        if existing_book is None:
            raise HTTPException(status_code=404, detail="Book not found")

        if existing_book.book_details is None:
            raise HTTPException(
                status_code=404, detail="Book details not found")

        return {"status": "success", "data": existing_book.book_details}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/books/{book_id}/details")
def delete_book_details(book_id: int, db: Session = Depends(get_db)):
    try:
        existing_book = views.get_book_by_id(book_id, db)

        if existing_book is None:
            raise HTTPException(status_code=404, detail="Book not found")

        if existing_book.book_details is None:
            raise HTTPException(
                status_code=404, detail="Book details not found")

        views.delete_book_details(book_id, db)
        return {"status": "success", "detail": "Book details deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
