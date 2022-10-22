

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
