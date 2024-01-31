from sqlalchemy.orm import Session
from Books.schema import BookCreate, BookUpdate, UserCreate, BorrowBook, ReturnBook
from Books.models import Book, BookDetails, User, BorrowedBook
import logging


# Book Management
def create_book(book_details: BookCreate, db: Session):
    try:
        book = Book(
            Title=book_details.title,
            ISBN=book_details.isbn,
            PublishedDate=book_details.published_date,
            Genre=book_details.genre,
        )

        # if book_details.details:
        #     book.book_details = BookDetails(
        #         NumberOfPages=book_details.details.NumberOfPages,
        #         Publisher=book_details.details.Publisher,
        #         Language=book_details.details.Language,
        #     )

        db.add(book)
        db.commit()
        db.refresh(book)
        logging.info(f"Book created successfully: {book}")
        return book
    except IntegrityError as e:
        # Duplicate ISBN, handle accordingly (log, raise exception, etc.)
        logging.error(f"Error creating book: {e}")
        db.rollback()
        raise HTTPException(status_code=400, detail="ISBN already exists")
    except Exception as e:
        logging.error(f"Error creating book: {e}")
        db.rollback()
        raise e


def get_book_by_id(book_id, db: Session):
    book = db.query(Book).filter(Book.BookID == book_id).first()
    if book:
        db.refresh(book)
    return book


def update_book(book_id, new_data, db: Session):
    try:
        book = db.query(Book).filter(Book.BookID == book_id).first()
        if book:
            for key, value in new_data.items():
                setattr(book, key, value)
            db.commit()
            db.refresh(book)
    except Exception as e:
        raise e


def delete_book(book_id, db: Session):
    try:
        book = db.query(Book).filter(Book.BookID == book_id).first()
        if book:
            db.delete(book)
            db.commit()
    except Exception as e:
        raise e


# User Management
def create_user(user_details: UserCreate, db: Session):
    try:
        user = User(
            Name=user_details.name,
            Email=user_details.email,
            MembershipDate=user_details.membership_date,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        raise e


def get_user_by_id(user_id, db: Session):
    user = db.query(User).filter(User.UserID == user_id).first()
    if user:
        db.refresh(user)
    return user


# Borrowed Books
def borrow_book(borrow_details: BorrowBook, db: Session):
    try:
        borrowed_book = BorrowedBook(
            UserID=borrow_details.user_id,
            BookID=borrow_details.book_id,
            BorrowDate=borrow_details.borrow_date,
        )
        db.add(borrowed_book)
        db.commit()
        db.refresh(borrowed_book)
        return borrowed_book
    except Exception as e:
        raise e


def return_book(return_details: ReturnBook, db: Session):
    try:
        borrowed_book = (
            db.query(BorrowedBook)
            .filter(
                BorrowedBook.UserID == return_details.user_id,
                BorrowedBook.BookID == return_details.book_id,
            )
            .first()
        )

        if borrowed_book:
            borrowed_book.ReturnDate = return_details.return_date
            db.commit()
            db.refresh(borrowed_book)
            return borrowed_book
        else:
            raise Exception("Borrowed book not found")
    except Exception as e:
        raise e


def list_all_borrowed_books(db: Session):
    borrowed_books = db.query(BorrowedBook).all()
    return borrowed_books
