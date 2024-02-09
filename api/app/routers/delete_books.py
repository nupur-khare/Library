from fastapi import APIRouter

from exceptions import AppException
from utils.delete_utils import Delete
from utils.login_utils import Login

router = APIRouter()


@router.delete("/deleteBook")
async def delete_book(book_name: str, username: str):
    user = Login.get_user(username)
    if user.get('role') != 'admin':
        raise AppException("Only admin users are allowed to access this endpoint!")
    Delete.validate_parameters(book_name)
    Delete.delete_book_from_csv(book_name)
    return {"message": f"Book '{book_name}' deleted successfully"}

