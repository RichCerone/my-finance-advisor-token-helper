import unittest

from src.token_helper.TokenHelper import TokenHelper, JWTError
from unittest.mock import patch

class CreateAccessTokenTests(unittest.TestCase):

    def setUp(self) -> None:
        self.secret_key = "some_secret"
        self.algo = "some_algo"
        self.access_token_expire_minutes = 5

    def tearDown(self) -> None:
        self.secret_key = None
        self.algo = None
        self.access_token_expire_minutes = None
    

    # Asserts the token is created.
    @patch("src.token_helper.TokenHelper.jwt")
    def test_create_access_token_creates_token(self, mock_jwt):
        mock_jwt.encode.return_value = "some_jwt"
        data = {"sub": "user_a"}

        token_helper = TokenHelper(self.secret_key, self.algo, self.access_token_expire_minutes)

        with self.assertLogs(level="DEBUG"):
            result = token_helper.create_access_token(data, True)

        self.assertIsNotNone(result)
        self.assertEqual("some_jwt", result)
        mock_jwt.encode.assert_called_once()


    # Asserts a JWTError is raised.
    @patch("src.token_helper.TokenHelper.jwt")
    def test_create_access_token_raises_jwt_error(self, mock_jwt):
        mock_jwt.encode.side_effect = JWTError()

        data = {"sub": "user_a"}

        token_helper = TokenHelper(self.secret_key, self.algo, self.access_token_expire_minutes)

        with self.assertLogs(level="ERROR"):
            with self.assertRaises(JWTError):
                token_helper.create_access_token(data, True)

        mock_jwt.encode.assert_called_once()


    # Asserts an exception is raised.
    @patch("src.token_helper.TokenHelper.jwt")
    def test_create_access_token_raises_exception(self, mock_jwt):
        mock_jwt.encode.side_effect = Exception()

        data = {"sub": "user_a"}

        token_helper = TokenHelper(self.secret_key, self.algo, self.access_token_expire_minutes)

        with self.assertLogs(level="ERROR"):
            with self.assertRaises(Exception):
                token_helper.create_access_token(data, True)

        mock_jwt.encode.assert_called_once()
