import hashlib
import os
import sys
import unittest

lobbit_app = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../")
sys.path.append(lobbit_app)

if lobbit_app in sys.path:
    from app.lobbit_util.crypto import LobbitHash


class TestCrypto(unittest.TestCase):
    """
    Test class for the Lobbit cryptographic classes
    """

    def setUp(self) -> None:
        """
        Setup test case variables
        """
        self.salt = os.urandom(16)
        self.wrong_length = LobbitHash(b'R8!Afh&f9k%', self.salt)
        self.no_lower = LobbitHash(b'JA$V139_R861BJ&E9U%3F', self.salt)
        self.no_upper = LobbitHash(b'ja$v139_r861bj&e9u%3f', self.salt)
        self.no_number = LobbitHash(b'ja$vAUT_rMopbj&eYu%Lf', self.salt)
        self.not_enough_symbols = LobbitHash(b'ja1vAU$T5rMo&pbj0eYu7Lf', self.salt)
        self.good_password = LobbitHash(b'ja%1v!AUT5rMopb$j0eY_u7Lf', self.salt)

    def test_LobbitHash_instantiates_correctly(self) -> None:
        """
        Test that the correct attributes are assigned when a LobbitHash
        instance is created
        """
        password = b'ja%1v!AUT5rMopb$j0eY_u7Lf'
        lh = LobbitHash(password, self.salt)
        self.assertEqual(lh.value, password)
        self.assertEqual(lh.salt, self.salt)

    def test_create_hash_returns_error_message(self) -> None:
        """
        Test that an error string is returned if creating the hash
        failed
        """
        error = self.wrong_length.create_hash()
        self.assertEqual(error[0], "Password complexity requirements not met. See help for more details")

    def test_create_hash_returns_Tuple(self) -> None:
        """
        Test that a Tuple is returned containing the salt and the
        salted hexdigest of the password
        """
        salt, hexdigest = self.good_password.create_hash()
        self.assertEqual(salt, self.salt)
        self.assertEqual(hexdigest, hashlib.sha3_256(b'ja%1v!AUT5rMopb$j0eY_u7Lf' + self.salt).hexdigest())

    def test_verify_password_returns_False_incorrect_length(self) -> None:
        """
        Tests that the verify_password returns False if the
        password is less than 12 characters long
        """
        self.assertFalse(self.wrong_length.verify_pw())

    def test_verify_password_returns_False_no_lowercase_letter(self) -> None:
        """
        Tests that the verify_password returns False if the
        password does not contain a lowercase letter
        """
        self.assertFalse(self.no_lower.verify_pw())

    def test_verify_password_returns_False_no_uppercase_letter(self) -> None:
        """
        Tests that the verify_password returns False if the
        password does not contain an uppercase letter
        """
        self.assertFalse(self.no_upper.verify_pw())

    def test_verify_password_returns_False_no_number(self) -> None:
        """
        Tests that the verify_password returns False if the
        password does not contain a number
        """
        self.assertFalse(self.no_number.verify_pw())

    def test_verify_password_returns_False_no_3_symbols(self) -> None:
        """
        Tests that the verify_password returns False if the
        password does not contain at least 3 symbols
        """
        self.assertFalse(self.not_enough_symbols.verify_pw())

    def test_verify_password_returns_True(self) -> None:
        """
        Tests that the verify_password returns True if the
        password matches the requirements
        """
        self.assertTrue(self.good_password.verify_pw())

    def test_verify_hash_returns_False_with_wrong_password(self) -> None:
        """
        Tests that verify_hash returns False is the password
        hashes do not match
        """
        wrong_lh = LobbitHash(b'27V$69yfg&o4wEuf_G81%73fn', self.salt)
        users_hash = hashlib.sha3_256(b'ja%1v!AUT5rMopb$j0eY_u7Lf' + self.salt).hexdigest()
        self.assertFalse(wrong_lh.verify_hash(users_hash))

    def test_verify_hash_returns_True_with_correct_password(self) -> None:
        """
        Tests that verify_hash returns True is the password
        hashes do match
        """
        users_hash = hashlib.sha3_256(b'ja%1v!AUT5rMopb$j0eY_u7Lf' + self.salt).hexdigest()
        self.assertTrue(self.good_password.verify_hash(users_hash))
