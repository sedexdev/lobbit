import argparse
import os
import socket
import unittest

from lobbit.client import (
    check_parse_errors,
    get_parser,
    LobbitClient,
    valid_ip,
    valid_path,
    valid_port
)


class TestClient(unittest.TestCase):
    """
    Test cases for the client application of the lobbit tool
    """

    def setUp(self) -> None:
        """
        Initialises test case variables
        """
        self.parser = get_parser()
        self.good_path = f"{os.path.abspath(os.path.dirname(__file__))}/blank"
        self.bad_path = f"{os.path.abspath(os.path.dirname(__file__))}/tank"
        self.lc = LobbitClient("172.16.0.10", 1234, [self.good_path])
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def tearDown(self) -> None:
        """
        Cleans up after testing
        """
        self.lc.sock.close()
        self.sock.close()

    def test_valid_ip_returns_ip(self) -> None:
        """
        Tests that the valid_ip function returns the IP address if a valid IP
        is passed in as a command line argument
        """
        ip = "192.168.0.1"
        is_valid_ip = valid_ip(ip)
        self.assertEqual(ip, is_valid_ip)

    def test_valid_ip_returns_false(self) -> None:
        """
        Tests that the valid_ip function returns False if an invalid IP
        is passed in as a command line argument
        """
        ip = "345.987.100.0"
        is_valid_ip = valid_ip(ip)
        self.assertFalse(is_valid_ip)

    def test_valid_port_returns_true(self) -> None:
        """
        Tests that the valid_port function returns True is a valid port
        number is passed in as an argument
        """
        self.assertTrue(valid_port(1234))

    def test_valid_port_returns_false(self) -> None:
        """
        Tests that the valid_port function returns False is an invalid port
        number is passed in as an argument
        """
        self.assertFalse(valid_port(66666))

    def test_valid_port_returns_false_when_non_integer_passed(self) -> None:
        """
        Tests that False is returned if a non-integer value is passed
        in as an argument
        """
        is_valid_port = valid_port("port_number")
        self.assertFalse(is_valid_port)

    def test_valid_path_returns_true(self) -> None:
        """
        Tests that the valid_path function returns True if a valid file
        path is passed in as an argument
        """
        is_valid_path = valid_path(self.good_path)
        self.assertTrue(is_valid_path)

    def test_valid_path_returns_false(self) -> None:
        """
        Tests that the valid_path function returns False if an invalid file
        path is passed in as an argument
        """
        is_valid_path = valid_path(self.bad_path)
        self.assertFalse(is_valid_path)

    def test_check_parse_errors_catches_bad_server_ip(self) -> None:
        """
        Tests that the check_parse_errors function calls a parser error if
        the server IP address is not a valid IPv4 address
        """
        with self.assertRaises(SystemExit) as se:
            args = self.parser.parse_args(["-i", "300.300.300.300", "-p", "1234", "-f", self.good_path])
            check_parse_errors(self.parser, args)
            self.assertEqual(se.exception.code, 2)

    def test_check_parse_errors_catches_bad_server_port(self) -> None:
        """
        Tests that the check_parse_errors function calls a parser error if
        the server port number is not valid
        """
        with self.assertRaises(SystemExit) as se:
            args = self.parser.parse_args(["-i", "192.168.0.10", "-p", "66666", "-f", self.good_path])
            check_parse_errors(self.parser, args)
            self.assertEqual(se.exception.code, 2)

    def test_check_parse_errors_catches_bad_file_paths(self) -> None:
        """
        Tests that the check_parse_errors function calls a parser error if
        any of the file paths passed are invalid
        """
        with self.assertRaises(SystemExit) as se:
            args = self.parser.parse_args(["-i", "192.168.0.10", "-p", "1234", "-f", self.bad_path])
            check_parse_errors(self.parser, args)
            self.assertEqual(se.exception.code, 2)

    def test_check_parse_errors_catch_empty_files_list(self) -> None:
        """
        Tests that the check_parse_errors function raises an error if
        the user doesn't pass in any file names to send
        """
        with self.assertRaises(SystemExit) as se:
            args = self.parser.parse_args(["-i", "192.168.0.10", "-p", "1234"])
            check_parse_errors(self.parser, args)
            self.assertEqual(se.exception.code, 2)

    def test_LobbitSocket_initialises_correctly(self) -> None:
        """
        Tests that a newly created instance of LobbitSocket has the correct
        attributes
        """
        self.assertEqual(self.lc.ip, "172.16.0.10")
        self.assertEqual(self.lc.port, 1234)
        self.assertEqual(self.lc.files, [self.good_path])
        self.assertEqual(type(self.lc.sock), type(self.sock))
        self.assertEqual(self.lc.delimiter, ":")
        self.assertEqual(self.lc.buffer_size, 4096)

    def test_get_file_sizes_returns_dictionary_with_correct_sizes(self) -> None:
        """
        Tests that filenames and sizes are sent back in the correct format
        """
        file_sizes = self.lc.get_file_sizes()
        expected = {"/storage/data/My_Work/Programming/Python/Python Projects/cmd_tools/lobbit/tests/blank": 0}
        self.assertEqual(file_sizes, expected)
