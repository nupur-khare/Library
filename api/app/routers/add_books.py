from fastapi import APIRouter

from exceptions import AppException
from utils.add_utils import Add
from utils.login_utils import Login

router = APIRouter()


@router.post("/addBook")
async def add_book(book_name: str, author: str, publication_year: int, username: str):
    user = Login.get_user(username)
    if user.get('role') != 'admin':
        raise AppException("Only admin users are allowed to access this endpoint!")
    Add.validate_parameters(book_name, author, publication_year)
    Add.add_book_to_csv(book_name, author, publication_year)
    return {"message": "Book added successfully!"}
