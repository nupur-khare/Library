from datetime import timedelta

from fastapi import HTTPException, Depends, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from api.models import Response
from shared.utils import Utility
from utils.login_utils import Login

router = APIRouter()
Utility.load_environment()


@router.post("/login", response_model=Response)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = Login.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=Utility.environment['jwt']["expiration"])
    access_token = Login.create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=access_token_expires
    )
    return {
        "data": {
            "access_token": access_token, "access_token_expiry": access_token_expires, "token_type": "bearer",
        }, "message": "User Authenticated",
    }
