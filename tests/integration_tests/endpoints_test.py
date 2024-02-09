from unittest import mock

import pytest
from fastapi.testclient import TestClient

from api.app.main import app
from exceptions import AppException
from shared.utils import Utility

client = TestClient(app)
Utility.load_environment()


def test_delete_book_success():
    book_name = "Book1"
    username = "admin"
    response = client.delete(f"/api/delete/deleteBook?book_name={book_name}&username={username}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Book '{book_name}' deleted successfully"}


def test_delete_book_invalid_user():
    book_name = "Book1"
    username = "regular"
    with pytest.raises(AppException, match="Only admin users are allowed to access this endpoint!"):
        response = client.delete(f"/api/delete/deleteBook?book_name={book_name}&username={username}")
        assert response.status_code != 200
        assert response.json() == {"detail": "Only admin users are allowed to access this endpoint!"}


def test_delete_book_invalid_params():
    book_name = 123
    username = "admin"
    response = client.delete(f"/api/delete/deleteBook?book_name={book_name}&username={username}")
    assert response.status_code == 200
    assert response.json() == {'message': "Book '123' deleted successfully"}


def test_add_book_success():
    book_name = "New Book"
    author = "Author Name"
    publication_year = 2022
    username = "admin"
    response = client.post(
        f"/api/add/addBook?book_name={book_name}&author={author}&publication_year={publication_year}&username={username}")
    assert response.status_code == 200
    assert response.json() == {"message": "Book added successfully!"}


def test_add_book_invalid_user():
    book_name = "New Book"
    author = "Author Name"
    publication_year = 2022
    username = "user"
    with pytest.raises(AppException, match="Only admin users are allowed to access this endpoint!"):
        response = client.post(
            f"/api/add/addBook?book_name={book_name}&author={author}&publication_year={publication_year}&username={username}")
        assert response.status_code != 200
        assert response.json() == {"detail": "Only admin users are allowed to access this endpoint!"}


def test_add_book_invalid_params():
    book_name = 123
    author = 456
    publication_year = "invalid"
    username = "admin"
    response = client.post(
        f"/api/add/addBook?book_name={book_name}&author={author}&publication_year={publication_year}&username={username}")
    assert response.status_code != 200


@mock.patch("utils.login_utils.Login.get_current_user", autospec=True)
def test_home_success_admin(mock_get_current_user):
    def _get_current_user(*args):
        return {
            "username": "admin",
            "password": "$2b$12$PErzM4f4RQ/NgSg7Ku9j0eL3mwLPld5sAy5SDu5pHEI/eznugbWcG",
            "disabled": False,
            "role": "admin"
        }

    mock_get_current_user.return_value = _get_current_user()
    token = "valid_admin_token"
    response = client.get(f"/api/fetch/home", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    actual = response.json()
    assert actual['success'] is True
    assert actual['message'] == 'Fetched books!'
    assert actual['data']['books'].__contains__("A Tale of Two Cities")


@mock.patch("utils.login_utils.Login.get_current_user", autospec=True)
def test_home_success_regular(mock_get_current_user):
    def _get_current_user(*args):
        return {
            "username": "abc",
            "password": "$2b$12$IZ5INWlV9tCJrooLjGB23u/Bg4pVY5LO6DdHy7pW8ywYVX0oRfv/m",
            "disabled": False,
            "role": "regular"
        }

    mock_get_current_user.return_value = _get_current_user()
    token = "valid_regular_token"
    response = client.get("/api/fetch/home", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    actual = response.json()
    assert actual['success'] is True
    assert actual['message'] == 'Fetched books!'
    assert actual['data']['books'].__contains__("A Tale of Two Cities")


def test_home_invalid_token():
    token = "invalid_token"
    response = client.get("/api/fetch/home", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


@mock.patch("utils.login_utils.Login.get_current_user", autospec=True)
@mock.patch("utils.home_utils.Home.read_books_from_csv", autospec=True)
def test_home_file_not_found(mock_read_books, mock_get_current_user):
    def _get_current_user(*args):
        return {
            "username": "abc",
            "password": "$2b$12$IZ5INWlV9tCJrooLjGB23u/Bg4pVY5LO6DdHy7pW8ywYVX0oRfv/m",
            "disabled": False,
            "role": "regular"
        }

    mock_get_current_user.return_value = _get_current_user()
    token = "valid_admin_token"
    mock_read_books.side_effect = FileNotFoundError
    with pytest.raises(AppException, match="File not found!"):
        response = client.get("/api/fetch/home", headers={"Authorization": f"Bearer {token}"})
        assert response


@mock.patch("utils.login_utils.Login.authenticate_user", autospec=True)
def test_login_success(mock_authenticate):
    mock_authenticate.return_value = {
        "username": "admin",
        "password": "$2b$12$PErzM4f4RQ/NgSg7Ku9j0eL3mwLPld5sAy5SDu5pHEI/eznugbWcG",
        "disabled": False,
        "role": "admin"
    }
    form_data = {"username": "admin", "password": "password123"}
    response = client.post("/api/auth/login", data=form_data)
    assert response.status_code == 200
    actual = response.json()
    assert actual['message'] == 'User Authenticated'
    assert actual['data']['token_type'] == 'bearer'
    assert actual['error_code'] == 0


def test_login_invalid_credentials():
    form_data = {"username": "invalid_user", "password": "invalid_password"}
    response = client.post("/api/auth/login", data=form_data)
    assert response.status_code == 401


def test_login_missing_credentials():
    form_data = {}
    response = client.post("/api/auth/login", data=form_data)
    assert response.status_code == 422
