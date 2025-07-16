import os
import socket
import sys
import threading
import unittest

lobbit_app = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../")
sys.path.append(lobbit_app)

if lobbit_app in sys.path:
    from app.lobbit_server.server import LobbitServer


class TestServer(unittest.TestCase):
    """
    Test cases for the server application of the lobbit tool
    """

    def setUp(self) -> None:
        """
        Initialises test case variables
        """
        self.ls = LobbitServer("127.0.0.1", 1234, "/test/path")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def tearDown(self) -> None:
        """
        Cleans up after tests
        """
        self.ls.sock.close()
        self.sock.close()

    @unittest.skipIf(os.getenv("GITHUB_ACTIONS") == "true", "Skipping due to missing SSL cert on runner")
    def test_lobbitServer_initialises_correctly(self) -> None:
        """
        Tests that the LobbitServer class has the correct attributes
        after initialisation
        """
        self.assertEqual(self.ls.host, "127.0.0.1")
        self.assertEqual(self.ls.port, 1234)
        self.assertEqual(self.ls.upload_path, "/test/path")
        self.assertEqual(type(self.ls.sock), type(self.sock))
        self.assertEqual(type(self.ls.thread_lock), type(threading.Lock()))
