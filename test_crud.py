# # tests/test_crud.py
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from Books.models import Book, User, BorrowedBook
# from Books.api import create_book, get_book_by_id, create_user, borrow_book, return_book, list_all_borrowed_books

# # Use an in-memory SQLite database for testing
# engine = create_engine('sqlite:///:memory:')
# Base = declarative_base()

# # Set up the test database
# Base.metadata.create_all(bind=engine)

# # Create a session to interact with the test database
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# db = SessionLocal()


# def test_create_book():
#     book_data = {
#         "title": "Test Book",
#         "isbn": "1234567890",
#         "published_date": "2022-01-31",
#         "genre": "Test Genre"
#     }
#     book = create_book(BookCreate(**book_data), db)
#     assert book is not None
#     assert book.Title == book_data["title"]


# def test_get_book_by_id():
#     book = get_book_by_id(1, db)
#     assert book is None  # Assuming there's no book with ID 1 in the test database


# def test_create_user():
#     user_data = {
#         "name": "Test User",
#         "email": "test@example.com",
#         "membership_date": "2022-01-31"
#     }
#     user = create_user(UserCreate(**user_data), db)
#     assert user is not None
#     assert user.Name == user_data["name"]


# def test_borrow_and_return_book():
#     borrow_data = {
#         "user_id": 1,
#         "book_id": 1,
#         "borrow_date": "2022-01-31"
#     }
#     borrowed_book = borrow_book(BorrowBook(**borrow_data), db)
#     assert borrowed_book is not None

#     return_data = {
#         "user_id": 1,
#         "book_id": 1,
#         "return_date": "2022-02-28"
#     }
#     returned_book = return_book(ReturnBook(**return_data), db)
#     assert returned_book is not None
#     assert returned_book.ReturnDate == return_data["return_date"]


# def test_list_all_borrowed_books():
#     borrowed_books = list_all_borrowed_books(db)
#     assert borrowed_books is not None
