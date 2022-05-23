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

    # def tearDown(self) -> None:
    #     """
    #     Cleans up after all tests have run
    #     """
    #     pass

    def test_LobbitREPL_class_initialises_correctly(self) -> None:
        """
        Tests that the correct attributes are assigned when
        a new instance of LobbitREPL is created
        """
        self.assertEqual(self.repl.prompt, "lobbit> ")
        self.assertEqual(self.repl.context, "base")
        self.assertEqual(self.repl.help, "help")
        self.assertEqual(self.repl.quit, "quit")
        self.assertEqual(self.repl.base_commands, ["set", "file", "user"])
        self.assertEqual(self.repl.set_subcmds, ["ip", "port"])
        self.assertEqual(self.repl.file_subcmds, ["add", "get", "remove", "move", "list", "upload"])
        self.assertEqual(self.repl.user_subcmds, ["create", "update", "delete"])
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

    def test_entering_only_help_command_displays_correct_help(self) -> None:
        """
        Tests that the help menu is displayed to the user in the
        'base' context if only the help command is entered
        """
        with patch('sys.stdout', new=StringIO()) as stdout:
            self.repl.cmd = "help"
            self.assertIn("set", stdout.getvalue())
            self.assertIn("file", stdout.getvalue())
            self.assertIn("user", stdout.getvalue())

    def test_entering_only_set_command_displays_correct_help(self) -> None:
        """
        Tests that the help menu is displayed to the user in the
        'set' context if only the set command is entered
        """
        with patch('sys.stdout', new=StringIO()) as stdout:
            self.repl.cmd = "set"
            self.assertIn("ip", stdout.getvalue())
            self.assertIn("port", stdout.getvalue())

    def test_entering_only_file_command_displays_correct_help(self) -> None:
        """
        Tests that the help menu is displayed to the user in the
        'file' context if only the file command is entered
        """
        with patch('sys.stdout', new=StringIO()) as stdout:
            self.repl.cmd = "file"
            self.assertIn("add", stdout.getvalue())
            self.assertIn("get", stdout.getvalue())
            self.assertIn("remove", stdout.getvalue())
            self.assertIn("move", stdout.getvalue())
            self.assertIn("list", stdout.getvalue())
            self.assertIn("upload", stdout.getvalue())

    def test_entering_only_user_command_displays_correct_help(self) -> None:
        """
        Tests that the help menu is displayed to the user in the
        'user' context if only the user command is entered
        """
        with patch('sys.stdout', new=StringIO()) as stdout:
            self.repl.cmd = "user"
            self.assertIn("create", stdout.getvalue())
            self.assertIn("update", stdout.getvalue())
            self.assertIn("delete", stdout.getvalue())
