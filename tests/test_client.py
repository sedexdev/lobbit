import os
import socket
import unittest

from lobbit.client import LobbitClient


class TestClient(unittest.TestCase):
    """
    Test cases for the client application of the lobbit tool
    """

    def setUp(self) -> None:
        """
        Initialises test case variables
        """
        self.path = f"{os.path.abspath(os.path.dirname(__file__))}/test_data/blank"
        self.lc = LobbitClient("172.16.0.10", 1234, [self.path])
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def tearDown(self) -> None:
        """
        Cleans up after testing
        """
        if self.lc.sock:
            self.lc.sock.close()
        self.sock.close()

    def test_LobbitSocket_initialises_correctly(self) -> None:
        """
        Tests that a newly created instance of LobbitSocket has the correct
        attributes
        """
        self.assertEqual(self.lc.ip, "172.16.0.10")
        self.assertEqual(self.lc.port, 1234)
        self.assertEqual(self.lc.files, [self.path])
        self.assertEqual(self.lc.sock, None)
