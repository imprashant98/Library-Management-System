from sqlalchemy.orm import Session
from Books.schema import BookDetailsBase, BookDetailsCreate, BookDetailsUpdate, BookBase, BookCreate, BookUpdate, UserBase, UserCreate, UserUpdate, BorrowBook, ReturnBook, BorrowedBookBase, BorrowedBookCreate, BorrowedBookUpdate, BorrowedBookResponse
from Books.models import Book, BookDetails, User, BorrowedBook
import logging
from passlib.hash import bcrypt
from sqlalchemy.exc import IntegrityError


# Book Management
def create_book(book_details: BookCreate, db: Session):
    try:
        book = Book(
            Title=book_details.title,
            ISBN=book_details.isbn,
            PublishedDate=book_details.published_date,
            Genre=book_details.genre,
        )

        if book_details.details:
            book.book_details = BookDetails(
                NumberOfPages=book_details.details.NumberOfPages,
                Publisher=book_details.details.Publisher,
                Language=book_details.details.Language,
            )

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

# Book Details Management


def create_book_details(book_id: int, book_details: BookDetailsCreate, db: Session):
    try:
        existing_book = db.query(Book).filter(Book.id == book_id).first()

        if existing_book is None:
            raise HTTPException(status_code=404, detail="Book not found")

        book_details_db = BookDetails(
            NumberOfPages=book_details.number_of_pages,
            Publisher=book_details.publisher,
            Language=book_details.language,
        )

        existing_book.book_details = book_details_db

        db.commit()
        db.refresh(existing_book)
        logging.info(
            f"Book details created successfully for Book ID {book_id}")
        return existing_book
    except Exception as e:
        logging.error(f"Error creating book details: {e}")
        db.rollback()
        raise e


def update_book_details(book_id: int, book_details: BookDetailsUpdate, db: Session):
    try:
        existing_book = db.query(Book).filter(Book.id == book_id).first()

        if existing_book is None:
            raise HTTPException(status_code=404, detail="Book not found")

        if existing_book.book_details is None:
            raise HTTPException(
                status_code=404, detail="Book details not found")

        for key, value in book_details.dict().items():
            setattr(existing_book.book_details, key, value)

        db.commit()
        db.refresh(existing_book)
        logging.info(
            f"Book details updated successfully for Book ID {book_id}")
        return existing_book
    except Exception as e:
        logging.error(f"Error updating book details: {e}")
        db.rollback()
        raise e


def read_book_details(book_id: int, db: Session):
    try:
        existing_book = db.query(Book).filter(Book.id == book_id).first()

        if existing_book is None:
            raise HTTPException(status_code=404, detail="Book not found")

        if existing_book.book_details is None:
            raise HTTPException(
                status_code=404, detail="Book details not found")

        db.refresh(existing_book)
        return existing_book.book_details
    except Exception as e:
        logging.error(f"Error reading book details: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def delete_book_details(book_id: int, db: Session):
    try:
        existing_book = db.query(Book).filter(Book.id == book_id).first()

        if existing_book is None:
            raise HTTPException(status_code=404, detail="Book not found")

        if existing_book.book_details is None:
            raise HTTPException(
                status_code=404, detail="Book details not found")

        db.delete(existing_book.book_details)
        db.commit()
        logging.info(
            f"Book details deleted successfully for Book ID {book_id}")
    except Exception as e:
        logging.error(f"Error deleting book details: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")

# User Management


def create_user(user_details: UserCreate, db: Session):
    try:
        hashed_password = bcrypt.hash(user_details.Password)
        user = User(
            Name=user_details.Name,
            Email=user_details.Email,
            Password=hashed_password,
            MembershipDate=user_details.MembershipDate,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
    except Exception as e:
        db.rollback()
        raise e


def get_user_by_id(user_id, db: Session):
    user = db.query(User).filter(User.UserID == user_id).first()
    if user:
        db.refresh(user)
    return user


def update_user(user_id: int, user_details: UserUpdate, db: Session):
    try:
        user = db.query(User).filter(User.UserID == user_id).first()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        for key, value in user_details.dict().items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
        logging.info(f"User updated successfully: {user}")
        return user
    except Exception as e:
        logging.error(f"Error updating user: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")


def delete_user(user_id: int, db: Session):
    try:
        user = db.query(User).filter(User.UserID == user_id).first()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(user)
        db.commit()
        logging.info(f"User deleted successfully: {user}")
    except Exception as e:
        logging.error(f"Error deleting user: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")

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
            logging.info(f"Book returned successfully: {borrowed_book}")
            return borrowed_book
        else:
            raise HTTPException(
                status_code=404, detail="Borrowed book not found")
    except Exception as e:
        logging.error(f"Error returning book: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")


def list_all_borrowed_books(db: Session):
    borrowed_books = db.query(BorrowedBook).all()
    return borrowed_books
