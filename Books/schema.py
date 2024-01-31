from typing import Optional
from pydantic import BaseModel
from datetime import date


class BookDetailsBase(BaseModel):
    NumberOfPages: Optional[int]
    Publisher: Optional[str]
    Language: Optional[str]


class BookDetailsCreate(BookDetailsBase):
    pass


class BookDetailsUpdate(BookDetailsBase):
    pass


class BookBase(BaseModel):
    title: str
    isbn: str
    published_date: date
    genre: str


class BookCreate(BookBase):
    details: Optional[BookDetailsCreate]


class BookUpdate(BookBase):
    details: Optional[BookDetailsUpdate]


class UserBase(BaseModel):
    Name: str
    Email: str
    Password: str
    MembershipDate: date


class UserLogin(BaseModel):
    Email: str
    Password: str


class UserCreate(UserBase):
    Password: str


class UserUpdate(UserBase):
    pass


class BorrowBook(BaseModel):
    user_id: int
    book_id: int
    borrow_date: date


class ReturnBook(BaseModel):
    user_id: int
    book_id: int
    return_date: date


class BorrowedBookBase(BaseModel):
    UserID: int
    BookID: int
    BorrowDate: date
    ReturnDate: Optional[date]


class BorrowedBookCreate(BorrowedBookBase):
    pass


class BorrowedBookUpdate(BorrowedBookBase):
    pass


class BorrowedBookResponse(BorrowedBookBase):
    id: int

    class Config:
        orm_mode = True
