#!/usr/bin/bash python3

import cmd
import ipaddress
import os
import sys

from typing import List, Tuple, Union

lobbit_module = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../")
sys.path.append(lobbit_module)

if lobbit_module in sys.path:
    from lobbit.client import LobbitClient


# noinspection PyArgumentList
class LobbitREPL(cmd.Cmd):

    intro_msg = "Welcome to the Lobbit File Transfer tool!"
    intro_spacer = "=" * len(intro_msg)
    intro = f"\n{intro_spacer}\n{intro_msg}\n{intro_spacer}\n"
    prompt = "\033[91m" + "lobbit> " + "\033[39m"

    def __init__(self) -> None:
        """
        Constructor for the REPLTest class
        """
        super().__init__()
        self.cmd_map = {
            "set": {
                "ip": self.handle_ip,
                "port": self.handle_port
            },
            "file": {
                "add": self.handle_add,
                "list": self.handle_list,
                "remove": self.handle_remove,
                "upload": self.handle_upload
            },
            "user": {
                "create": self.handle_create,
                "update": self.handle_update,
                "delete": self.handle_delete
            }
        }
        self.client = None
        self.ip = None
        self.port = None
        self.files = []

    # --- OVERLOADED CMD METHODS ---

    def completedefault(self, text: str, line: str, begidx: int, endidx: int) -> List:
        """
        Provides tab completion for commands without a <complete_*()>
        method associated with them

        Args:
            text (str)   : the string prefix to match
            line (str)   : the current input line
            begidx (int) : beginning index of the prefix text
            endidx (int) : end index of the prefix text
        Returns:
            List : a List of matches for non-completed commands
        """
        tokens = line.split()
        if tokens[0].strip() == "set":
            return self.sub_cmd_matches("set", text)
        if tokens[0].strip() == "file":
            return self.sub_cmd_matches("file", text)
        if tokens[0].strip() == "user":
            return self.sub_cmd_matches("user", text)
        return []

    def emptyline(self) -> None:
        """
        Default action when no argument is entered on the
        command line
        """
        return

    def default(self, line: str) -> None:
        """
        Default output when a user inputs incorrect syntax

        Args:
             line (str) : the current input line
        """
        self.error("Unknown command entered")

    # --- UTILITY METHODS ---

    def split_args(self, args: str) -> Union[List, None]:
        """
        Splits the command arguments into a List and returns
        the List to the calling method

        Args:
            args (str) : the base command arguments passed in by the user
        Returns:
            List : the arguments split on whitespace or None
        """
        if not args:
            self.error(f"Incomplete command: '{self.lastcmd} ...'")
            return
        return args.split(" ")

    def sub_cmd_matches(self, base_cmd: str, text: str) -> List:
        """
        This helper method allows the program to apply the
        autocomplete feature to sub-commands as well

        Args:
            base_cmd (str) : base command to check sub-commands for
            text (str)     : the command passed in
        Returns:
            List : a list of matches found or an empty list
        """
        matches = []
        n = len(text)
        sub_cmds = self.cmd_map.get(base_cmd).keys()
        for word in sub_cmds:
            if word[:n] == text:
                matches.append(word)
        return matches

    @staticmethod
    def error(msg: str) -> None:
        """
        Displays a message to the user in response to invalid input

        Args:
             msg (str)  : message to display
        """
        print(f"[-] Error: {msg}")

    # --- DO METHODS ---

    @staticmethod
    def do_quit(_) -> None:
        """
        Quits the program with a 0 exit status and prints a
        message to the user
        """
        print("Bye!")
        sys.exit(0)

    def do_set(self, arg: str) -> None:
        """
        Sets a network parameter used to create a connection
        to the server over an AF_INET instance of <socket.socket>

        Args:
            arg (str) : the base command arguments passed in by the user
        """
        args = self.split_args(arg)
        if not args:
            return
        sub_cmds = self.cmd_map.get("set")
        if args[0] not in sub_cmds.keys():
            self.error(f"'{args[0]}' is not a valid sub-command of 'set'")
            return
        try:
            sub_cmds.get(args[0])(args[1])
        except IndexError:
            arg_name = "<ipv4_address>" if args[0] == "ip" else "<port_number>"
            self.error(f"'{self.lastcmd}' missing required argument: {arg_name}")

    def do_file(self, arg: str) -> None:
        """
        Allows the user to add files to <self.files> for uploading, list
        out the files that have been added, or upload the files
        in <self.files>

        Args:
            arg (str) : the base command arguments passed in by the user
        """
        args = self.split_args(arg)
        if not args:
            return
        sub_cmds = self.cmd_map.get("file")
        if args[0] not in sub_cmds.keys():
            self.error(f"'{args[0]}' is not a valid sub-command of 'file'")
            return
        if args[0] == "add" or args[0] == "remove":
            sub_cmds.get(args[0])(args[1:])
        else:
            sub_cmds.get(args[0])()

    # TODO

    def do_user(self, arg: str) -> None:
        """
        Allows the user to create and modify users. This method works
        in conjunction with the <LobbitAPI> class that should be
        running on the server instance to create, update, and delete
        users from the backend database. Security is handled using the
        classes in crypto.py

        Args:
            arg (str) : the base command arguments passed in by the user
        """
        self.split_args(arg)

    def do_net(self, _) -> None:
        """
        Shows the current network socket configuration
        """
        print(f"IPv4 Address: {self.ip}")
        print(f"Port number : {self.port}")

    def do_help(self, arg: str) -> None:
        """
        Shows the help menu

        Args:
            arg (str) : the base command arguments passed in by the user
        """
        print("\n==== LOBBIT HELP MENU ====\n"
              "\nBase commands:\n"
              "  set  - Set the value of a required network parameter\n"
              "  file - perform an action on a file or list of files\n"
              "  user - perform an action on a user object\n"
              "  net  - display the current remote network parameters\n"
              "\nSet commands:\n"
              "  ip [IP_ADDRESS]    - set the IPv4 address of the remote server (REQUIRED)\n"
              "  port [PORT_NUMBER] - set the port of the remote server (REQUIRED)\n"
              "\nFile commands:\n"
              "  add [FILE_PATHS] - add a file to the list of files to be uploaded\n"
              "  list             - list the files you have added for upload\n"
              "  remove [INDEXES] - remove a file from the upload list\n"
              "  upload           - upload the files you have added\n"
              "\nUser commands:\n"
              "  create <username> <password> - create a new user\n"
              "  update <username> <password> - update a password for an existing user\n"
              "  delete <username>            - delete an existing user\n"
              "\nExamples:\n"
              "  Set IPv4 address                       : set ip 100.200.0.1\n"
              "  Add 2 files for upload                 : file add /path/to/file1 /another/path/to/file2\n"
              "  Remove added files at indexes 1 and 3  : file remove 1 3\n"
              "  Change user password                   : user update <username> <password>\n")

    # --- VALIDATION METHODS ---

    def valid_ip(self) -> Union[str, bool]:
        """
        Checks that the value of <self.ip> is a valid IPv4 address

        Returns:
            str : the value of <ip> if a ValueError is not raised
        """
        try:
            return str(ipaddress.ip_address(self.ip))
        except ValueError:
            return False

    def valid_port(self) -> bool:
        """
        Checks that the value of <port> is an integer from 1-65535

        Returns:
            bool : True if valid, False if not
        """
        try:
            return 1 <= int(self.port) <= 65535
        except TypeError:
            return False
        except ValueError:
            return False

    @staticmethod
    def valid_path(file_path: str) -> Tuple:
        """
        Checks the system path passed in as <file_path> to ensure
        that a valid file object can be found at the path

        Args:
            file_path (str) : the path to validate
        Returns:
            bool : True is path is a file, False if not
        """
        try:
            if os.path.isabs(file_path):
                path = file_path
            else:
                path = f"{os.getcwd()}/{file_path}"
            if os.path.isfile(path):
                return True, path
            return False, None
        except TypeError:
            return False, None

    # --- ACTION HANDLERS ---

    def handle_ip(self, ip: str) -> None:
        """
        Process the set ip command

        Args:
            ip (str) : ip address passed into 'set ip'
        """
        self.ip = ip
        if not self.valid_ip():
            self.error(f"Invalid IPv4 address: '{ip}'")
            self.ip = None
            return

    def handle_port(self, port: int) -> None:
        """
        Process the set port command

        Args:
            port (int) : port number passed into 'set port'
        """
        self.port = int(port)
        if not self.valid_port():
            self.error(f"Invalid port number: '{port}'")
            self.port = None
            return

    def handle_add(self, files: List) -> None:
        """
        Process the file add command

        Args:
            files (List) : file paths to be added to the upload list
        """
        if not files:
            self.error(f"'{self.lastcmd}' missing required argument: <file_path(s)>")
            return
        for file in files:
            path_tuple = self.valid_path(file)
            if not path_tuple[0]:
                self.files = []
                self.error(f"{file} is not valid file path. The upload list has not been modified")
                return
            else:
                self.files.append(path_tuple[1])

    def handle_list(self) -> None:
        """
        Process the file list command
        """
        if not self.files:
            self.error("No files have been added for upload")
            return
        for index, file in enumerate(self.files):
            print(f"[{index}] {file}")

    def handle_remove(self, indices: List) -> None:
        """
        Process the file remove command

        Args:
             indices (List) : indexes of the element to remove
        """
        indices = sorted(indices, reverse=True)
        for index in indices:
            try:
                if int(index) < len(self.files):
                    self.files.pop(int(index))
            except IndexError:
                self.error(f"Chosen index '{index}' is out of bounds")
            except ValueError:
                self.error("Index must be of type 'int'")

    def handle_upload(self) -> None:
        """
        Process the file upload command
        """
        if not self.files:
            self.error("No files have been added for upload")
            return
        if not self.ip and not self.port:
            self.error("Invalid network parameters")
            return
        client = LobbitClient(self.ip, self.port, self.files)
        client.lobbit_connect()
        client.lobbit_send()

    # TODO

    @staticmethod
    def handle_create() -> None:
        """
        Process the user create command
        """
        print("Handling user create")

    @staticmethod
    def handle_update() -> None:
        """
        Process the user update command
        """
        print("Handling user update")

    @staticmethod
    def handle_delete() -> None:
        """
        Process the user delete command
        """
        print("Handling user delete")


if __name__ == '__main__':
    try:
        repl = LobbitREPL()
        repl.cmdloop()
    except KeyboardInterrupt:
        print("\nBye!")
        sys.exit(0)
