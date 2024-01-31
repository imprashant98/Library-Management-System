# Library Management System API

This FastAPI application is a comprehensive system for managing a book library, utilizing a PostgreSQL database and SQLAlchemy for seamless interactions. It includes functionality for adding, updating, and deleting books, as well as retrieving detailed information about each book.

The API provides endpoints for book management, user-related operations, and tracking borrowed books. Users can add new books, retrieve book details by ID, update book information, and delete books from the library. Additionally, the system allows users to add new members, retrieve user details by ID, and manage borrowed books, including borrowing and returning.

The underlying database consists of tables for books, book details, users, and borrowed books, with defined relationships to maintain data integrity. The SQLAlchemy ORM facilitates database interactions, ensuring smooth communication between the FastAPI application and the PostgreSQL database.

To use this API, clients can make HTTP requests to the specified endpoints, receiving JSON responses. The API supports operations such as adding books, retrieving book details, updating book information, deleting books, managing users, borrowing books, returning books, and listing all borrowed books.

Developers can interact with the API using tools like Postman or cURL, allowing for efficient testing and integration into larger systems. The system is built on a robust foundation, combining FastAPI, SQLAlchemy, and PostgreSQL to deliver a reliable and scalable solution for library management.

# Installation

- To get started, clone this repository to your local machine:

`git clone git@github.com:imprashant98/LibraryMS.git`

`cd libraryms`

- Create a virtual environment and install the dependencies:

`python -m venv env`

`source env/bin/activate` # On Windows use `env\Scripts\activate`

`pip install -r requirements.txt`

# Usage

Run `uvicorn main:app --reload`

This will start the server on `http://127.0.0.1:8000`. You can access the API documentation by visiting `http://127.0.0.1:8000/docs` in your web browser.

In addition to the API, the project includes functionality to manage books. The API supports operations such as adding, updating, deleting, and retrieving books from a database. Each book is defined by attributes such as title, ISBN, published date, genre, and additional details.

# How to Interact with the API

- **Add a Book:** Use the `/books/add/` endpoint with a POST request, providing the required details.
- **Get Book by ID:** Access the `/books/{book_id}` endpoint with a GET request to retrieve details for a specific book.
- **Update Book:** Utilize the `/books/{book_id}` endpoint with a PUT request to update information for a specific book.
- **Delete Book:** Make a DELETE request to `/books/{book_id}` to remove a book from the database.
- **Add User:** Use the `/users/add/` endpoint to add a new user.
- **Get User by ID:** Access the `/users/{user_id}` endpoint to retrieve details for a specific user.
- **Borrow Book:** Send a POST request to `/borrow` to borrow a book.
- **Return Book:** Use the `/return` endpoint with a POST request to return a borrowed book.
- **List Borrowed Books:** Access the `/borrowed-books` endpoint with a GET request to retrieve a list of all borrowed books.

Feel free to experiment with the API using tools like Postman or curl.
