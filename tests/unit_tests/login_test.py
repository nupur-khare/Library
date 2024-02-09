import unittest
from datetime import timedelta
from unittest import mock
from unittest.mock import patch

import jwt
from fastapi import HTTPException, status

from utils.login_utils import Login


class TestLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.username = "admin"
        cls.password = "adminpassword"
        cls.fake_user = {
            "username": cls.username,
            "password": Login.pwd_context.hash(cls.password),
            "disabled": False,
            "role": "admin"
        }
        cls.valid_token_data = {"sub": cls.username, "role": "admin"}

    def test_verify_password_correct(self):
        hashed_password = self.fake_user["password"]
        result = Login.verify_password(self.password, hashed_password)
        self.assertTrue(result)

    def test_verify_password_incorrect(self):
        hashed_password = self.fake_user["password"]
        result = Login.verify_password("wrongpassword", hashed_password)
        self.assertFalse(result)

    def test_get_user_exists(self):
        result = Login.get_user(self.username)
        assert result['username'] == self.fake_user.get('username')

    def test_get_user_not_exists(self):
        result = Login.get_user("nonexistentuser")
        assert result == {}

    @mock.patch("utils.login_utils.Login.verify_password", autospec=True)
    def test_authenticate_user_success(self, mock_verify_pswd):
        mock_verify_pswd.return_value = True
        result = Login.authenticate_user(self.username, self.password)
        assert result['username'] == 'admin'

    def test_authenticate_user_failure(self):
        result = Login.authenticate_user(self.username, "wrongpassword")
        self.assertFalse(result)

    def test_create_access_token(self):
        expires_delta = timedelta(minutes=30)
        encoded_jwt = Login.create_access_token(self.valid_token_data, expires_delta)
        assert encoded_jwt is not None

    @patch('jwt.decode')
    async def test_get_current_user_success(self, mock_decode):
        mock_decode.return_value = {"sub": self.username}
        result = await Login.get_current_user("validtoken")
        self.assertEqual(result, self.fake_user)

    @patch('jwt.decode')
    async def test_get_current_user_expired_token(self, mock_decode):
        mock_decode.side_effect = jwt.ExpiredSignatureError
        with self.assertRaises(HTTPException) as context:
            await Login.get_current_user("expiredtoken")
        self.assertEqual(context.exception.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('jwt.decode')
    async def test_get_current_user_invalid_token(self, mock_decode):
        mock_decode.side_effect = jwt.PyJWTError
        with self.assertRaises(HTTPException) as context:
            await Login.get_current_user("invalidtoken")
        self.assertEqual(context.exception.status_code, status.HTTP_401_UNAUTHORIZED)
