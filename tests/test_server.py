import socket
import unittest

from lobbit.server import LobbitServer


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

    def test_LobbitServer_initialises_correctly(self) -> None:
        """
        Tests that the LobbitServer class has the correct attributes
        after initialisation
        """
        self.assertEqual(self.ls.ip, "127.0.0.1")
        self.assertEqual(self.ls.port, 1234)
        self.assertEqual(self.ls.upload_path, "/test/path")
        self.assertEqual(type(self.ls.sock), type(self.sock))
        self.assertEqual(self.ls.client_sock, None)

    def test_lobbit_receive_exits_when_client_sock_is_not_initialised(self) -> None:
        """
        Tests to make sure that the lobbit_receive method exits with
        a status of 2 if the <self.client_sock> attribute is not
        initialised
        """
        with self.assertRaises(SystemExit) as se:
            self.ls.lobbit_receive()
            self.assertEqual(se.exception.code, 2)
