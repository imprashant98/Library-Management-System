from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from config.db_config import engine

Base = declarative_base()


class Book(Base):
    __tablename__ = "books"

    BookID = Column(Integer, primary_key=True)
    Title = Column(String, nullable=False)
    ISBN = Column(String, unique=True, nullable=False)
    PublishedDate = Column(Date)
    Genre = Column(String)

    # Define the one-to-one relationship with BookDetails
    book_details = relationship(
        "BookDetails",
        uselist=False,
        back_populates="book",
    )


class BookDetails(Base):
    __tablename__ = "book_details"

    DetailsID = Column(Integer, primary_key=True)
    NumberOfPages = Column(Integer)
    Publisher = Column(String)
    Language = Column(String)

    # Define the one-to-one relationship with Book
    book_id = Column(Integer, ForeignKey("books.BookID"),
                     unique=True, nullable=False)

    # Define the back reference to the Book entity
    book = relationship(
        "Book",
        back_populates="book_details",
    )


class User(Base):
    __tablename__ = "users"

    UserID = Column(Integer, primary_key=True)
    Name = Column(String, nullable=False)
    Email = Column(String, unique=True, nullable=False)
    Password = Column(String, nullable=False)
    MembershipDate = Column(Date)


class BorrowedBook(Base):
    __tablename__ = "borrowed_books"

    BorrowedBookID = Column(Integer, primary_key=True)
    UserID = Column(Integer, ForeignKey("users.UserID"), nullable=False)
    BookID = Column(Integer, ForeignKey("books.BookID"), nullable=False)
    BorrowDate = Column(Date, nullable=False)
    ReturnDate = Column(Date)

    # Define the many-to-one relationship with User
    user = relationship("User", back_populates="borrowed_books")

    # Define the many-to-one relationship with Book
    book = relationship("Book", back_populates="borrowed_books")


# Add the back references to User and Book
User.borrowed_books = relationship("BorrowedBook", back_populates="user")
Book.borrowed_books = relationship("BorrowedBook", back_populates="book")

# make migrations
Base.metadata.create_all(bind=engine)
