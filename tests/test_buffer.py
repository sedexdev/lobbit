import os
import socket
import sys
import unittest

lobbit_app = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../")
sys.path.append(lobbit_app)

if lobbit_app in sys.path:
    from app.lobbit_util.buffer import Buffer


class TestBuffer(unittest.TestCase):
    """
    Test class for the Buffer class
    """

    def setUp(self) -> None:
        """
        Initialises test case variables
        """
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_buffer = Buffer(self.client_sock)

    def tearDown(self) -> None:
        """
        Cleans up after testing
        """
        self.client_sock.close()

    def test_class_initialises_correctly(self) -> None:
        """
        Tests that the correct class attributes are assigned when
        the Buffer class is instantiated
        """
        self.assertEqual(self.client_sock, self.client_buffer.sock)
        self.assertEqual(b'', self.client_buffer.buffer)
