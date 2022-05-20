import hashlib
import os


class LobbitHash:
    """
    Class that exposes a few basic hash related methods
    """

    def create_hash(self, value: bytes) -> str:
        """
        Takes in a byte string and generates a 256bit hash digest
        using the SHA-256 hash function. The salt is pulled from
        the database and used to compare the data in <value> to
        the value stored in the database

        Args:
            value (bytes) : byte string to be hashed
        Returns:
            str : the hash digest of the value
        """
        pass

    def verify_hash(self, x: str, y: str) -> bool:
        """
        Args:
            x (str) : the hash of the value sent by the user
            y (str) : the stored hash value to compare x against
        Returns:
            bool : boolean verifying whether the 2 values x and y match
        """
        pass


class LobbitEncrypt:
    """
    Class that exposes methods for working with AES encryption,
    secure key exchange, and public key security associations
    """

    def __init__(self, data: bytes, key: bytes) -> None:
        """
        Constructor for the LobbitEncrypt class

        Args:
            data : the data to be encrypted
            key  : the symmetric encryption key
        """
        pass

    def encrypt(self) -> bytes:
        """
        Encrypts the data supplied by the user

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
