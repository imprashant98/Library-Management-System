from urllib.parse import quote_plus
from fastapi import Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Books import views
from Books.schema import BookDetailsBase, UserLogin, BookDetailsCreate, BookDetailsUpdate, BookBase, BookCreate, BookUpdate, UserBase, UserCreate, UserUpdate, BorrowBook, ReturnBook, BorrowedBookBase, BorrowedBookCreate, BorrowedBookUpdate, BorrowedBookResponse
from config.db_config import SessionLocal
from pydantic import BaseModel
from fastapi import FastAPI, Body
from Books.auth.auth_bearer import JWTBearer
from Books.auth.auth_handler import signJWT
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from decouple import config


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


# Define the OAuth2PasswordBearer for token validation
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# JWT Configuration
JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

# Function to decode JWT token


def decode_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception


# Book Management
@router.post("/books/add/")
def create_book(book_details: BookCreate, db: Session = Depends(get_db), current_user: dict = Depends(decode_token)):
    user_id = current_user.get("user_id")
    if user_id:
        return views.create_book(book_details, db, user_id)
    else:
        raise HTTPException(status_code=401, detail="Authentication required")


@router.get("/books/{book_id}")
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = views.get_book_by_id(book_id, db)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/books/{book_id}")
def update_book(book_id: int, new_data: dict, db: Session = Depends(get_db), current_user: dict = Depends(decode_token)):
    user_id = current_user.get("user_id")
    if user_id:
        book = views.update_book(book_id, new_data, db, user_id)
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return book
    else:
        raise HTTPException(status_code=401, detail="Authentication required")


@router.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: dict = Depends(decode_token)):
    user_id = current_user.get("user_id")
    if user_id:
        success = views.delete_book(book_id, db, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="Book not found")
        return {"detail": "Book deleted successfully"}
    else:
        raise HTTPException(status_code=401, detail="Authentication required")

# User Management


def check_user(data: UserBase, db: Session = Depends(get_db)):
    user = views.get_user_by_email(data.Email, db)

    if user and views.verify_user_password(data.Password, user.Password):
        return user
    return None


@router.post("/users/login")
def login_user(data: UserLogin, db: Session = Depends(get_db)):
    user = check_user(data, db)

    if user:
        jwt_token = signJWT(user.Email)
        return {"status": "success", "token": jwt_token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/users/add/")
def add_user(user_details: UserCreate, db: Session = Depends(get_db)):
    try:
        user = views.create_user(user_details, db)
        jwt_token = signJWT(user.Email)
        return {"status": "success", "data": user, "token": jwt_token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db), current_user: dict = Depends(decode_token)):
    if current_user.get("user_id") == user_id:
        user = views.get_user_by_id(user_id, db)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {"status": "success", "data": user}
    else:
        raise HTTPException(status_code=401, detail="Authentication required")


@router.put("/users/{user_id}")
def update_user(user_id: int, user_details: dict, db: Session = Depends(get_db), current_user: dict = Depends(decode_token)):
    if current_user.get("user_id") == user_id:
        user = views.update_user(user_id, user_details, db)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {"status": "success", "data": user}
    else:
        raise HTTPException(status_code=401, detail="Authentication required")


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: dict = Depends(decode_token)):
    if current_user.get("user_id") == user_id:
        success = views.delete_user(user_id, db)
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        return {"detail": "User deleted successfully"}
    else:
        raise HTTPException(status_code=401, detail="Authentication required")

# Borrowed Books


@router.post("/borrow")
def borrow_book(borrow_details: BorrowBook, db: Session = Depends(get_db), current_user: dict = Depends(decode_token)):
    user_id = current_user.get("user_id")
    if user_id:
        try:
            borrowed_book = views.borrow_book(borrow_details, db, user_id)
            return {"status": "success", "data": borrowed_book}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=401, detail="Authentication required")


@router.post("/return")
def return_book(return_details: ReturnBook, db: Session = Depends(get_db), current_user: dict = Depends(decode_token)):
    user_id = current_user.get("user_id")
    if user_id:
        try:
            returned_book = views.return_book(return_details, db, user_id)
            return {"status": "success", "data": returned_book}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=401, detail="Authentication required")


@router.get("/borrowed-books")
def list_borrowed_books(db: Session = Depends(get_db), current_user: dict = Depends(decode_token)):
    user_id = current_user.get("user_id")
    if user_id:
        borrowed_books = views.list_all_borrowed_books(db, user_id)
        return {"status": "success", "data": borrowed_books}
    else:
        raise HTTPException(status_code=401, detail="Authentication required")

# Books Details


@router.post("/books/{book_id}/details")
def create_book_details(book_id: int, book_details: BookDetailsCreate, db: Session = Depends(get_db), current_user: dict = Depends(decode_token)):
    user_id = current_user.get("user_id")
    if user_id:
        try:
            existing_book = views.get_book_by_id(book_id, db)

            if existing_book is None:
                raise HTTPException(status_code=404, detail="Book not found")

            book = views.create_book_details(
                book_id, book_details, db, user_id)
            return {"status": "success", "data": book}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=401, detail="Authentication required")


@router.put("/books/{book_id}/details")
def update_book_details(book_id: int, book_details: BookDetailsUpdate, db: Session = Depends(get_db), current_user: dict = Depends(decode_token)):
    user_id = current_user.get("user_id")
    if user_id:
        try:
            existing_book = views.get_book_by_id(book_id, db)

            if existing_book is None:
                raise HTTPException(status_code=404, detail="Book not found")

            if existing_book.book_details is None:
                raise HTTPException(
                    status_code=404, detail="Book details not found")

            book = views.update_book_details(
                book_id, book_details, db, user_id)
            return {"status": "success", "data": book}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=401, detail="Authentication required")


@router.get("/books/{book_id}/details")
def read_book_details(book_id: int, db: Session = Depends(get_db), current_user: dict = Depends(decode_token)):
    user_id = current_user.get("user_id")
    if user_id:
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
    else:
        raise HTTPException(status_code=401, detail="Authentication required")


@router.delete("/books/{book_id}/details")
def delete_book_details(book_id: int, db: Session = Depends(get_db), current_user: dict = Depends(decode_token)):
    user_id = current_user.get("user_id")
    if user_id:
        try:
            existing_book = views.get_book_by_id(book_id, db)

            if existing_book is None:
                raise HTTPException(status_code=404, detail="Book not found")

            if existing_book.book_details is None:
                raise HTTPException(
                    status_code=404, detail="Book details not found")

            views.delete_book_details(book_id, db, user_id)
            return {"status": "success", "detail": "Book details deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=401, detail="Authentication required")
