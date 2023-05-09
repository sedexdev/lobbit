#!/usr/bin/bash python3

import cmd
import ipaddress
import os
import sys

from typing import List, Tuple, Union

lobbit_app = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../../")
sys.path.append(lobbit_app)

if lobbit_app in sys.path:
    from app.lobbit_client.client import LobbitClient


# noinspection PyArgumentList
class LobbitREPL(cmd.Cmd):

    intro_msg = "Welcome to the Lobbit File Transfer tool!"
    intro_spacer = "=" * len(intro_msg)
    intro = f"\n{intro_spacer}\n{intro_msg}\n{intro_spacer}\n"
    prompt = "\033[91m" + "lobbit> " + "\033[39m"

    def __init__(self) -> None:
        """
        Constructor for the LobbitREPL class
        """
        super().__init__()
        self.cmd_map = {
            "set": {
                "ip": self.handle_ip,
                "hostname": self.handle_hostname,
                "port": self.handle_port
            },
            "file": {
                "add": self.handle_add,
                "list": self.handle_list,
                "remove": self.handle_remove,
                "upload": self.handle_upload
            },
            "use": {
                "hostname": self.set_hostname,
                "ip": self.set_ip
            }
        }
        self.client = None
        self.host = None
        self.port = None
        self.files = []
        self.hostname = False

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
        if tokens[0].strip() == "use":
            return self.sub_cmd_matches("use", text)
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

    # TODO
    #   - check bug with command history
    #   - when history gets a command with a '.', the
    #     start of the command is left after the prompt

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
        if len(args) > 2:
            self.error(f"set {args[0]} expects 1 argument")
            return
        try:
            sub_cmds.get(args[0])(args[1])
        except IndexError:
            for arg in sub_cmds.keys():
                if args[0] == arg:
                    self.error(f"'{self.lastcmd}' missing required argument: {arg}")
                    return

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

    def do_use(self, arg: str) -> None:
        """
        Allows the user to use either the remote machine's hostname or IP
        address to create the connection. Use the boolean value of <self.hostname>
        to toggle between options

        Args:
            arg (str) : the base command arguments passed in by the user
        """
        args = self.split_args(arg)
        if not args:
            return
        sub_cmds = self.cmd_map.get("use")
        if args[0] not in sub_cmds.keys():
            self.error(f"'{args[0]}' is not a valid sub-command of 'use'")
            return
        if len(args) > 1:
            self.error(f"Unexpected arguments '{args[1:]}' after {args[0]}")
            return
        sub_cmds.get(args[0])()

    def do_net(self, _) -> None:
        """
        Shows the current network socket configuration
        """
        if self.hostname:
            print(f"Hostname: {self.host}")
        else:
            print(f"IPv4 Address: {self.host}")
        print(f"Port number: {self.port}")

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
              "  use  - use either 'hostname' or 'ip' for the remote connection\n"
              "  net  - display the current remote network parameters\n"
              "\nSet commands:\n"
              "  ip [IP_ADDRESS]    - set the IPv4 address of the remote server (REQUIRED)\n"
              "  port [PORT_NUMBER] - set the port of the remote server (REQUIRED)\n"
              "\nFile commands:\n"
              "  add [FILE_PATHS] - add one or more file paths to the list of files to be uploaded\n"
              "  list             - list the files you have added for upload\n"
              "  remove [INDEXES] - remove a file from the upload list\n"
              "  upload           - upload the files you have added\n"
              "\nUse commands:\n"
              "  hostname - use a hostname for the remote connection\n"
              "  ip       - use an IP address for the remote connection\n"
              "\nExamples:\n"
              "  Set IPv4 address                       : set ip 100.200.0.1\n"
              "  Add 2 files for upload                 : file add /path/to/file1 /another/path/to/file2\n"
              "  Remove added files at indexes 1 and 3  : file remove 1 3\n"
              "  Use hostname instead of IP to connect  : use hostname\n")

    # --- VALIDATION METHODS ---

    def valid_ip(self) -> Union[str, bool]:
        """
        Checks that the value of <self.host> is a valid IPv4 address

        Returns:
            str : the value of <ip> if a ValueError is not raised
        """
        try:
            return str(ipaddress.ip_address(self.host))
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
        if self.hostname:
            self.error("Current settings require a hostname")
            return
        self.host = ip
        if not self.valid_ip():
            self.error(f"Invalid IPv4 address: '{ip}'")
            self.host = None
            return

    def handle_hostname(self, hostname: str) -> None:
        """
        Processes the set hostname command

        Args:
            hostname (str): hostname passed into 'set hostname'
        """
        if not self.hostname:
            self.error("Current settings require an IP address")
            return
        self.host = hostname

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
        if not len(self.files):
            self.error("The upload list is currently empty...")
            return
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
        if not self.host and not self.port:
            self.error("Invalid network parameters")
            return
        client = LobbitClient(self.host, self.port, self.files)
        connection = client.lobbit_connect()
        if connection:
            client.lobbit_send()

    def set_hostname(self) -> None:
        """
        Sets the socket connection host to a hostname
        """
        self.host = None
        self.hostname = True

    def set_ip(self) -> None:
        """
        Sets the socket connection host to an IP address
        """
        self.host = None
        self.hostname = False


if __name__ == '__main__':
    try:
        repl = LobbitREPL()
        repl.cmdloop()
    except KeyboardInterrupt:
        print("\nBye!")
        sys.exit(0)
