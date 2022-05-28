import os
import unittest

from io import StringIO
from unittest.mock import patch
from lobbit.repl import LobbitREPL


class TestLobbitREPL(unittest.TestCase):
    """
    Test class for the LobbitREPL class
    """

    def setUp(self) -> None:
        """
        Initialises test case variables
        """
        self.repl = LobbitREPL()
        self.good_path = f"{os.path.abspath(os.path.dirname(__file__))}/test_data/blank"
        self.bad_path = f"{os.path.abspath(os.path.dirname(__file__))}/test_data/tank"

    def test_LobbitREPL_class_initialises_correctly(self) -> None:
        """
        Tests that the correct attributes are assigned when
        a new instance of LobbitREPL is created
        """
        self.assertEqual(self.repl.prompt, "lobbit> ")
        self.cmd_map = {
            "set": {
                "ip": self.repl.handle_ip,
                "port": self.repl.handle_port
            },
            "file": {
                "add": self.repl.handle_add,
                "get": self.repl.handle_get,
                "remove": self.repl.handle_remove,
                "move": self.repl.handle_move,
                "list": self.repl.handle_list,
                "upload": self.repl.handle_upload
            },
            "user": {
                "create": self.repl.handle_create,
                "update": self.repl.handle_update,
                "delete": self.repl.handle_delete
            }
        }
        self.assertEqual(self.repl.cmd, None)
        self.assertEqual(self.repl.args, None)
        self.assertEqual(self.repl.client, None)
        self.assertEqual(self.repl.ip, "")
        self.assertEqual(self.repl.port, -1)
        self.assertEqual(self.repl.files, [])

    def test_quit_command_exits_repl(self) -> None:
        """
        Tests that the program exists with a system status of 1
        when the command 'quit' is entered
        """
        with self.assertRaises(SystemExit) as se:
            self.repl.cmd = "quit"
            self.repl.run()
            self.assertEqual(se.exception.code, 1)

    def test_is_base_cmd_returns_true(self) -> None:
        """
        Tests that the is_base_cmd method returns True if
        a valid base command is passed in
        """
        self.assertTrue(self.repl.is_base_cmd("set"))

    def test_is_base_cmd_returns_false(self) -> None:
        """
        Tests that the is_base_cmd method returns False if
        an invalid base command is passed in
        """
        self.assertFalse(self.repl.is_base_cmd("test"))

    def test_is_sub_cmd_returns_true(self) -> None:
        """
        Tests that the is_sub_cmd method returns True if a valid
        sub command is passed in
        """
        self.assertTrue(self.repl.is_sub_cmd("ip"))

    def test_is_sub_cmd_returns_false(self) -> None:
        """
        Tests that the is_sub_cmd method returns False if
        an invalid sub command is passed in
        """
        self.assertFalse(self.repl.is_sub_cmd("test"))

    def test_handle_single_cmd_method_displays_help(self) -> None:
        """
        Tests that the handle_single_cmd method displays the help
        text when the command 'help' is types
        """
        self.repl.cmd = "help"
        with patch("sys.stdout", new=StringIO()) as stdout:
            self.repl.handle_single_cmd()
            self.assertIn("\n==== LOBBIT HELP MENU ====\n", stdout.getvalue())

    def test_handle_single_cmd_method_displays_incomplete_command(self) -> None:
        """
        Tests that the handle_single_cmd method displays an error
        message when a single command is entered
        """
        self.repl.cmd = "set"
        with patch("sys.stdout", new=StringIO()) as stdout:
            self.repl.handle_single_cmd()
            self.assertIn("Incomplete input", stdout.getvalue())

    def test_handle_single_cmd_method_displays_unknown_command(self) -> None:
        """
        Tests that the handle_single_cmd method displays an error
        message when a single unknown command is entered
        """
        self.repl.cmd = "test"
        with patch("sys.stdout", new=StringIO()) as stdout:
            self.repl.handle_single_cmd()
            self.assertIn("unknown command", stdout.getvalue())

    def test_valid_ip_returns_ip(self) -> None:
        """
        Tests that the valid_ip function returns the IP address if a valid IP
        is passed in as a command line argument
        """
        self.repl.ip = "172.16.0.1"
        is_valid_ip = self.repl.valid_ip()
        self.assertEqual(self.repl.ip, is_valid_ip)

    def test_valid_ip_returns_false(self) -> None:
        """
        Tests that the valid_ip function returns False if an invalid IP
        is passed in as a command line argument
        """
        is_valid_ip = self.repl.valid_ip()
        self.assertFalse(is_valid_ip)

    def test_valid_port_returns_true(self) -> None:
        """
        Tests that the valid_port function returns True is a valid port
        number is passed in as an argument
        """
        self.repl.port = 1234
        self.assertTrue(self.repl.valid_port())

    def test_valid_port_returns_false(self) -> None:
        """
        Tests that the valid_port function returns False is an invalid port
        number is passed in as an argument
        """
        self.assertFalse(self.repl.valid_port())

    def test_valid_path_returns_true(self) -> None:
        """
        Tests that the valid_path function returns True if a valid file
        path is passed in as an argument
        """
        self.repl.files.append(f"{os.path.abspath(os.path.dirname(__file__))}/test_data/blank")
        is_valid_path = self.repl.valid_path()
        self.assertTrue(is_valid_path)

    def test_valid_path_returns_false(self) -> None:
        """
        Tests that the valid_path function returns False if an invalid file
        path is passed in as an argument
        """
        is_valid_path = self.repl.valid_path()
        self.assertFalse(is_valid_path)

    def test_valid_path_returns_false_with_wrong_value(self) -> None:
        """
        Tests that the valid_path function returns False if an invalid type
        is passed in as an argument
        """
        self.repl.files.append(100)
        is_valid_path = self.repl.valid_path()
        self.assertFalse(is_valid_path)

    def test_handle_ip_sets_ip_correctly(self) -> None:
        """
        Tests that the handle_ip method sets the <self.ip> attribute
        correctly when a valid IPv4 address is passed as an argument
        """
        self.repl.cmd = "set ip 192.168.0.1"
        self.repl.parse_cmd(self.repl.cmd.split(" "))
        self.assertEqual(self.repl.ip, "192.168.0.1")

    def test_handle_ip_sets_ip_back_to_empty_string(self) -> None:
        """
        Tests that the handle_ip method sets the <self.ip> attribute
        back to an empty string when an invalid IPv4 address is passed as
        an argument
        """
        self.repl.cmd = "set ip test"
        self.repl.parse_cmd(self.repl.cmd.split(" "))
        self.assertEqual(self.repl.ip, "")

    def test_handle_ip_sets_port_correctly(self) -> None:
        """
        Tests that the handle_port method sets the <self.port> attribute
        correctly when a valid port number is passed as an argument
        """
        self.repl.cmd = "set port 1234"
        self.repl.parse_cmd(self.repl.cmd.split(" "))
        self.assertEqual(self.repl.port, 1234)

    def test_handle_ip_sets_port_back_to_empty_string(self) -> None:
        """
        Tests that the handle_port method sets the <self.port> attribute
        back to an empty string when an invalid port number is passed as
        an argument
        """
        self.repl.cmd = "set port 123456789"
        self.repl.parse_cmd(self.repl.cmd.split(" "))
        self.assertEqual(self.repl.port, -1)
