# Library Management System

## Overview
This project is a simple library management system built using FastAPI, designed to manage books and users with different roles (admin and regular user). It provides endpoints for authentication, adding, deleting, and fetching books from the library.

## Features
- **User Authentication**: Authenticate users with admin and regular roles using JWT tokens.
- **Manage Books**: Admin users can add and delete books from the library.
- **Fetch Books**: Users can view the list of available books in the library.

## Installation
Clone the repository: `git clone https://github.com/your_username/library-management.git`

## API Endpoints
- **POST /api/auth/login**: Authenticate users and obtain JWT token.
- **POST /api/add/addBook**: Add a new book to the library (admin only).
- **DELETE /api/delete/deleteBook**: Delete a book from the library (admin only).
- **GET /api/fetch/home**: Fetch the list of books from the library.

## Usage
1. Authenticate as admin or regular user using the login endpoint.
2. Use the obtained JWT token to access the protected endpoints.
3. Admin users can add and delete books using the respective endpoints.
4. Regular users can view the list of available books using the fetch books endpoint.

## Technologies Used.
- Python: Programming language
- FastAPI: Web framework for building APIs with Python.
- JWT: Token-based authentication for securing endpoints.
- Pandas: Library for data manipulation and CSV file handling.

## Testing Commands
- To run unit tests, command -> python -m pytest tests/unit_tests
- To run integration tests, command -> python -m pytest tests/integration_tests
