import hashlib
import os
import sys
import unittest

lobbit_app = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../")
sys.path.append(lobbit_app)

if lobbit_app in sys.path:
    from app.lobbit_util.crypto import LobbitEncrypt


class TestCrypto(unittest.TestCase):
    """
    Test class for the Lobbit cryptographic classes
    """

    def setUp(self) -> None:
        """
        Setup test case variables
        """
        pass
