import unittest

from src.token_helper.TokenHelper import TokenHelper, JWTError, JWTClaimsError, ExpiredSignatureError
from unittest.mock import patch

class DecodeAccessTokenTets(unittest.TestCase):
    
    def setUp(self) -> None:
        self.secret_key = "some_secret"
        self.algo = "some_algo"
        self.access_token_expire_minutes = 5

    def tearDown(self) -> None:
        self.secret_key = None
        self.algo = None
        self.access_token_expire_minutes = None

    
    # Assert a token is decoded.
    @patch("src.token_helper.TokenHelper.jwt")
    def test_decode_access_token_decodes_token(self, mock_jwt):
        mock_jwt.decode.return_value = { 
            "sub": "user"
        }

        token_helper = TokenHelper(self.secret_key, self.algo, self.access_token_expire_minutes)

        with self.assertLogs(level="DEBUG"):
            result = token_helper.decode_access_token("some_token")

        self.assertEqual("user", result)
        mock_jwt.decode.assert_called_once()

    
    # Asserts a JWTClaimsError is raised.
    @patch("src.token_helper.TokenHelper.jwt")
    def test_decode_access_token_raises_jwt_claim_error(self, mock_jwt):
        mock_jwt.decode.side_effect = JWTClaimsError()

        token_helper = TokenHelper(self.secret_key, self.algo, self.access_token_expire_minutes)

        with self.assertLogs(level="DEBUG"):
            with self.assertRaises(JWTClaimsError):
                token_helper.decode_access_token("some_token")

        mock_jwt.decode.assert_called_once()


    # Asserts a ExpiredSignatureError is raised.
    @patch("src.token_helper.TokenHelper.jwt")
    def test_decode_access_token_raises_expired_signature_error(self, mock_jwt):
        mock_jwt.decode.side_effect = ExpiredSignatureError()

        token_helper = TokenHelper(self.secret_key, self.algo, self.access_token_expire_minutes)

        with self.assertLogs(level="DEBUG"):
            with self.assertRaises(ExpiredSignatureError):
                token_helper.decode_access_token("some_token")

        mock_jwt.decode.assert_called_once()

    
    # Asserts a JWTError is raised.
    @patch("src.token_helper.TokenHelper.jwt")
    def test_decode_access_token_raises_jwt_error(self, mock_jwt):
        mock_jwt.decode.side_effect = JWTError()

        token_helper = TokenHelper(self.secret_key, self.algo, self.access_token_expire_minutes)

        with self.assertLogs(level="DEBUG"):
            with self.assertRaises(JWTError):
                token_helper.decode_access_token("some_token")

        mock_jwt.decode.assert_called_once()