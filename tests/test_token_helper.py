import unittest

from src.token_helper.TokenHelper import TokenHelper

class TokenHelperTests(unittest.TestCase):

    # Asserts TokenHelper can be initialized.
    def test_token_handler_inits(self):
        token_helper = TokenHelper("some_key", "some_algo", 5)

        self.assertIsInstance(token_helper, TokenHelper)

    
    # Asserts a ValueError is raised.
    def test_token_handler_raises_value_error(self):
        with self.assertRaises(ValueError):
            TokenHelper(" ", "some_algo", 5)

        with self.assertRaises(ValueError):
            TokenHelper(None, "some_algo", 5)
        
        with self.assertRaises(ValueError):
            TokenHelper(" ", "some_algo", 5)

        with self.assertRaises(ValueError):
            TokenHelper("some_secret", None, 5)