from pydantic import BaseModel
from datetime import datetime


class BookDetailsBase(BaseModel):
    NumberOfPages: int
    Publisher: str
    Language: str


class BookCreate(BaseModel):
    title: str
    isbn: str
    published_date: datetime
    genre: str
    details: BookDetailsBase


class BookUpdate(BaseModel):
    title: str
    isbn: str
    published_date: datetime
    genre: str


class UserCreate(BaseModel):
    name: str
    email: str
    membership_date: datetime


class BorrowBook(BaseModel):
    user_id: str
    book_id: str
    borrow_date: datetime


class ReturnBook(BaseModel):
    user_id: str
    book_id: str
    return_date: datetime
