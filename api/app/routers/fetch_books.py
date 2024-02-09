from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer

from api.models import Response
from exceptions import AppException
from utils.home_utils import Home
from utils.login_utils import Login

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/home", response_model=Response)
async def home(token: str = Depends(oauth2_scheme)):
    user = await Login.get_current_user(token)
    user_type = user.get('role')
    if user_type == "admin":
        file_paths = ["/home/nupur_khare/PycharmProjects/Library/data/regular_users.csv",
                      "/home/nupur_khare/PycharmProjects/Library/data/admin_users.csv"]
    else:
        file_paths = ["/home/nupur_khare/PycharmProjects/Library/data/regular_users.csv"]
    try:
        book_names = Home.read_books_from_csv(file_paths)
    except FileNotFoundError:
        raise AppException("File not found!")
    return {"data": {"books": book_names},
            "message": "Fetched books!"}
