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
        self.good_path = f"{os.path.abspath(os.path.dirname(__file__))}/test_data/blank"
        self.bad_path = f"{os.path.abspath(os.path.dirname(__file__))}/test_data/tank"
        self.lc = LobbitClient("172.16.0.10", 1234, [self.good_path])
        self.lc_bad = LobbitClient("333.444.555.666", 8712113, [self.bad_path])
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def tearDown(self) -> None:
        """
        Cleans up after testing
        """
        if self.lc.sock:
            self.lc.sock.close()
        self.sock.close()

    def test_valid_ip_returns_ip(self) -> None:
        """
        Tests that the valid_ip function returns the IP address if a valid IP
        is passed in as a command line argument
        """
        is_valid_ip = self.lc.valid_ip()
        self.assertEqual(self.lc.ip, is_valid_ip)

    def test_valid_ip_returns_false(self) -> None:
        """
        Tests that the valid_ip function returns False if an invalid IP
        is passed in as a command line argument
        """
        is_valid_ip = self.lc_bad.valid_ip()
        self.assertFalse(is_valid_ip)

    def test_valid_port_returns_true(self) -> None:
        """
        Tests that the valid_port function returns True is a valid port
        number is passed in as an argument
        """
        self.assertTrue(self.lc.valid_port())

    def test_valid_port_returns_false(self) -> None:
        """
        Tests that the valid_port function returns False is an invalid port
        number is passed in as an argument
        """
        self.assertFalse(self.lc_bad.valid_port())

    def test_valid_path_returns_true(self) -> None:
        """
        Tests that the valid_path function returns True if a valid file
        path is passed in as an argument
        """
        is_valid_path = self.lc.valid_path()
        self.assertTrue(is_valid_path)

    def test_valid_path_returns_false(self) -> None:
        """
        Tests that the valid_path function returns False if an invalid file
        path is passed in as an argument
        """
        is_valid_path = self.lc_bad.valid_path()
        self.assertFalse(is_valid_path)

    def test_LobbitSocket_initialises_correctly(self) -> None:
        """
        Tests that a newly created instance of LobbitSocket has the correct
        attributes
        """
        self.assertEqual(self.lc.ip, "172.16.0.10")
        self.assertEqual(self.lc.port, 1234)
        self.assertEqual(self.lc.files, [self.good_path])
        self.assertEqual(self.lc.sock, None)
        self.assertEqual(self.lc.delimiter, "<DELIMITER>")
        self.assertEqual(self.lc.buffer_size, 4096)

    def test_get_file_sizes_returns_dictionary_with_correct_sizes(self) -> None:
        """
        Tests that filenames and sizes are sent back in the correct format
        """
        file_sizes = self.lc.get_file_sizes()
        expected = {
            f"{os.path.abspath(os.path.dirname(__file__))}/test_data/blank": 0
        }
        self.assertEqual(file_sizes, expected)
