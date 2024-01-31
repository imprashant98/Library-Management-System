# Library Management System API

This FastAPI application is a comprehensive system for managing a book library, utilizing a PostgreSQL database and SQLAlchemy for seamless interactions. It includes functionality for adding, updating, and deleting books, as well as retrieving detailed information about each book.

The API provides endpoints for book management, user-related operations, and tracking borrowed books. Users can add new books, retrieve book details by ID, update book information, and delete books from the library. Additionally, the system allows users to add new members, retrieve user details by ID, and manage borrowed books, including borrowing and returning.

The underlying database consists of tables for books, book details, users, and borrowed books, with defined relationships to maintain data integrity. The SQLAlchemy ORM facilitates database interactions, ensuring smooth communication between the FastAPI application and the PostgreSQL database.

To use this API, clients can make HTTP requests to the specified endpoints, receiving JSON responses. The API supports operations such as adding books, retrieving book details, updating book information, deleting books, managing users, borrowing books, returning books, and listing all borrowed books.

Developers can interact with the API using tools like Postman or cURL, allowing for efficient testing and integration into larger systems. The system is built on a robust foundation, combining FastAPI, SQLAlchemy, and PostgreSQL to deliver a reliable and scalable solution for library management.

# Installation

- To get started, clone this repository to your local machine:

`https://github.com/imprashant98/Library-Management-System.git`

`cd library-management-system`

- Create a virtual environment and install the dependencies:

`python -m venv venv`

`source venv/bin/activate` # On Windows use `venv\Scripts\activate`

`pip install -r requirements.txt`

# Usage

Run `uvicorn main:app --reload`

This will start the server on `http://127.0.0.1:8000`. You can access the API documentation by visiting `http://127.0.0.1:8000/docs` in your web browser.

In addition to the API, the project includes functionality to manage books. The API supports operations such as adding, updating, deleting, and retrieving books from a database. Each book is defined by attributes such as title, ISBN, published date, genre, and additional details.

# How to Interact with the API

1. **JWT Configuration:**

   - JWT (JSON Web Tokens) are used for authentication.
   - Configuration includes a secret key (`JWT_SECRET`) and an algorithm (`JWT_ALGORITHM`).

2. **Token Validation:**

   - A `decode_token` function validates and decodes JWT tokens.
   - It is used as a dependency for protected endpoints.

3. **Book Management:**

   - **Add a Book:**

     - Endpoint: `POST /books/add/`
     - Creates a new book in the system.

   - **Get Book by ID:**

     - Endpoint: `GET /books/{book_id}`
     - Retrieves details for a specific book based on its ID.

   - **Update Book:**

     - Endpoint: `PUT /books/{book_id}`
     - Updates information for a specific book based on its ID.

   - **Delete Book:**
     - Endpoint: `DELETE /books/{book_id}`
     - Removes a book from the database based on its ID.

4. **User Management:**

   - **User Login:**

     - Endpoint: `POST /users/login`
     - Authenticates a user using email and password, returning a JWT token upon success.

   - **Add User:**

     - Endpoint: `POST /users/add/`
     - Adds a new user to the system.

   - **Get User by ID:**

     - Endpoint: `GET /users/{user_id}`
     - Retrieves details for a specific user based on their ID.

   - **Update User:**

     - Endpoint: `PUT /users/{user_id}`
     - Updates information for a specific user based on their ID.

   - **Delete User:**
     - Endpoint: `DELETE /users/{user_id}`
     - Removes a user from the system based on their ID.

5. **Borrowed Books:**

   - **Borrow Book:**

     - Endpoint: `POST /borrow`
     - Allows users to borrow a book.

   - **Return Book:**

     - Endpoint: `POST /return`
     - Enables users to return a borrowed book.

   - **List Borrowed Books:**
     - Endpoint: `GET /borrowed-books`
     - Retrieves a list of all borrowed books.

6. **Book Details:**

   - **Add Book Details:**

     - Endpoint: `POST /books/{book_id}/details`
     - Creates details for a specific book based on its ID.

   - **Update Book Details:**

     - Endpoint: `PUT /books/{book_id}/details`
     - Updates details for a specific book based on its ID.

   - **Get Book Details:**

     - Endpoint: `GET /books/{book_id}/details`
     - Retrieves details for a specific book based on its ID.

   - **Delete Book Details:**
     - Endpoint: `DELETE /books/{book_id}/details`
     - Removes details for a specific book based on its ID.

7. **Usage:**
   - Make requests using tools like Postman or curl.
   - Include the JWT token in the Authorization header for protected endpoints.

# Login

Use the `/users/login` endpoint with a POST request to authenticate a user and obtain a JWT token.

# Authentication

This API also uses JSON Web Tokens (JWT) for authentication. JWT is a compact, URL-safe means of representing claims to be transferred between two parties.

Feel free to experiment with the API using tools like Postman or curl.
