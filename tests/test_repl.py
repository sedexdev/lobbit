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

    def test_LobbitREPL_class_initialises_correctly(self) -> None:
        """
        Tests that the correct attributes are assigned when
        a new instance of LobbitREPL is created
        """
        self.assertEqual(self.repl.prompt, "lobbit> ")
        self.assertEqual(self.repl.set_subcmds, ["ip", "port"])
        self.assertEqual(self.repl.file_subcmds, ["add", "get", "remove", "move", "list", "upload"])
        self.assertEqual(self.repl.user_subcmds, ["create", "update", "delete"])
        self.assertEqual(self.repl.cmd_map, {
            "set": self.repl.set_subcmds,
            "file": self.repl.file_subcmds,
            "user": self.repl.user_subcmds
        })
        self.assertEqual(self.repl.cmd, None)
        self.assertEqual(self.repl.client, None)
        self.assertEqual(self.repl.ip, None)
        self.assertEqual(self.repl.port, None)
        self.assertEqual(self.repl.files, None)

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

    def test_set_value_assigns_attribute_values_correctly(self) -> None:
        """
        Tests that the set_value method correctly assigns IPv4 addresses
        and port numbers
        """
        self.repl.set_value("127.0.0.1", "ip")

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
