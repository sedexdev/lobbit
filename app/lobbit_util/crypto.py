import hashlib
import string

from typing import Tuple


class LobbitHash:
    """
    Class that exposes a few basic hash related methods
    """

    def __init__(self, value: bytes, salt: bytes):
        """
        Constructor for the LobbitHash class

        Args:
            value (bytes) : the users password
            salt (bytes)  : salt to add to the hash
        """
        self.value = value
        self.salt = salt

    def create_hash(self) -> Tuple:
        """
        Takes in a byte string and generates a 256bit hash digest
        using the SHA-256 hash function. The salt is pulled from
        the database and used to compare the test_data in <value> to
        the value stored in the database

        Returns:
            str : the hash digest of the value
        """
        verified = self.verify_pw()
        if not verified:
            return "Password complexity requirements not met. See help for more details",
        return self.salt, hashlib.sha3_256(self.value + self.salt).hexdigest()

    def verify_pw(self) -> bool:
        """
        Verifies that the password matches complexity requirements.
        The password must:
            - be at least 12 characters long
            - contain a lowercase and uppercase letter
            - contain a numerical character
            - contain at least 3 symbols
        """
        if len(self.value) < 12:
            return False
        if not any(i for i in self.value.decode() if i.islower()):
            return False
        if not any(i for i in self.value.decode() if i.isupper()):
            return False
        if not any(i for i in self.value.decode() if i.isdigit()):
            return False
        if len([i for i in string.punctuation if i in self.value.decode()]) < 3:
            return False
        return True

    def verify_hash(self, users_hash: str) -> bool:
        """
        Compares the salted hash value of the password provided by the
        user to the one stored against the user in the database

        Args:
            users_hash (str) : existing hash of users salted password

        Returns:
            bool : boolean verifying whether the passwords match
        """
        pw_hash = hashlib.sha3_256(self.value + self.salt).hexdigest()
        return pw_hash == users_hash


class LobbitEncrypt:
    """
    Class that exposes methods for working with AES encryption,
    secure key exchange, and public key security associations
    """

    def __init__(self, data: bytes, key: bytes) -> None:
        """
        Constructor for the LobbitEncrypt class

        Args:
            data : the test_data to be encrypted
            key  : the symmetric encryption key
        """
        pass

    def encrypt(self) -> bytes:
        """
        Encrypts the test_data supplied by the user

        Returns:
            bytes : an encrypted byte string of ciphertext
        """
        pass

    def decrypt(self) -> str:
        """
        Decrypts the ciphertext

        Returns:
            str : a string of plaintext
        """
        pass
