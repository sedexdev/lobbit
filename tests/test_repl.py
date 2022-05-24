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
        self.cmd_map = {
            "reset": [],
            "set": self.repl.set_subcmds,
            "file": self.repl.file_subcmds,
            "user": self.repl.user_subcmds
        }
        self.assertEqual(self.repl.cmd, None)

    def test_quit_command_exits_repl(self) -> None:
        """
        Tests that the program exists with a system status of 1
        when the command 'quit' is entered
        """
        with self.assertRaises(SystemExit) as se:
            self.repl.cmd = "quit"
            self.repl.run()
            self.assertEqual(se.exception.code, 1)

    def test_is_base_cmd_returns_value(self) -> None:
        """
        Tests that the is_base_cmd method returns its value parameter if
        a valid base command is passed in
        """
        cmd = self.repl.is_base_cmd("set")
        self.assertEqual(cmd, "set")

    def test_is_base_cmd_prints_alert(self) -> None:
        """
        Tests that the is_base_cmd method prints an alert if an invalid
        base command is passed in
        """
        self.repl.is_base_cmd("test")
        with patch('sys.stdout', new=StringIO()) as stdout:
            self.assertIn(stdout.getvalue(), "unknown command")

    def test_is_sub_cmd_returns_tuple(self) -> None:
        """
        Tests that the is_sub_cmd method returns a tuple if a valid
        sub command is passed in
        """
        cmd = self.repl.is_sub_cmd("ip")
        self.assertEqual(cmd, ("set", "ip"))

    def test_is_sub_cmd_prints_alert(self) -> None:
        """
        Tests that the is_sub_cmd method prints an alert if an invalid
        sub command is passed in
        """
        self.repl.is_sub_cmd("test")
        with patch('sys.stdout', new=StringIO()) as stdout:
            self.assertIn(stdout.getvalue(), "unknown command")

    def test_set_value_assigns_attribute_values_correctly(self) -> None:
        """
        Tests that the set_value method correctly assigns IPv4 addresses
        and port numbers
        """
        self.repl.set_value("127.0.0.1", "ip")
