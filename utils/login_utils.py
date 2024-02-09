from datetime import timedelta, datetime

import jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from shared.utils import Utility


class Login:
    Utility.load_environment()
    fake_users = {"users": [{
            "username": "admin",
            "password": "$2b$12$PErzM4f4RQ/NgSg7Ku9j0eL3mwLPld5sAy5SDu5pHEI/eznugbWcG",
            "disabled": False,
            "role": "admin"
        },
        {
            "username": "abc",
            "password": "$2b$12$IZ5INWlV9tCJrooLjGB23u/Bg4pVY5LO6DdHy7pW8ywYVX0oRfv/m",
            "disabled": False,
            "role": "regular"
        },
        {
            "username": "xyz",
            "password": "$7b$12$IZ5INWlV9tCKcooLjGB23u/Bg4pVY5LO6DdHy7pW8ywYVX0oRfv/m",
            "disabled": False,
            "role": "regular"
        }
    ]
        }

    # JWT settings
    token_expire_minutes = Utility.environment['jwt']["expiration"]
    secret_key = Utility.environment['jwt']["jwt_secret_key"]
    algorithm = Utility.environment['jwt']["jwt_algorithm"]

    # Password hashing
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    @staticmethod
    def verify_password(plain_password, hashed_password):
        """
         Verifies password
        :param plain_password: plain password
        :param hashed_password: hashes password
        """
        return Login.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_user(username: str):
        """
        Fetches user with username
        :param username: username
        :return: user dictionary
        """
        user_dict = {}
        for user in Login.fake_users['users']:
            if user.get('username') == username:
                user_dict = user
        return user_dict

    @staticmethod
    def authenticate_user(username: str, password: str):
        """
        Authenticates user
        :param username: username
        :param password: password
        :return: user
        """
        user = Login.get_user(username)
        if not user or not Login.verify_password(password, user["password"]):
            return False
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None):
        """
        Creates access token
        :param data: user details
        :param expires_delta: time
        :return: encoded token
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=Login.token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, Login.secret_key, algorithm=Login.algorithm)
        return encoded_jwt

    @staticmethod
    async def get_current_user(token: str = Depends(oauth2_scheme)):
        """
        Authenticates user with OAuth2
        :param token: token
        :return: user
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, Login.secret_key, algorithms=[Login.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except jwt.ExpiredSignatureError:
            raise credentials_exception
        except jwt.PyJWTError:
            raise credentials_exception

        user = Login.get_user(username)
        if user is None:
            raise credentials_exception
        return user
