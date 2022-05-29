#!/usr/bin/bash python3

import ipaddress
import os
import sys

from typing import List, Union

lobbit_module = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../")
sys.path.append(lobbit_module)

if lobbit_module in sys.path:
    from lobbit.client import LobbitClient


class LobbitREPL:
    """
    Class that implements the functionality of a terminal-based
    Read Evaluate Print Loop. The REPL is used to configure the
    network connection and add the files to be sent to the
    server
    """

    def __init__(self) -> None:
        """
        Constructor for the LobbitREPL class
        """
        self.prompt = "\033[91m" + "lobbit> " + "\033[39m"
        self.cmd_map = {
            "set": {
                "ip": self.handle_ip,
                "port": self.handle_port
            },
            "file": {
                "add": self.handle_add,
                "list": self.handle_list,
                "upload": self.handle_upload
            },
            "user": {
                "create": self.handle_create,
                "update": self.handle_update,
                "delete": self.handle_delete
            }
        }
        self.cmd = None
        self.args = None
        self.client = None
        self.ip = ""
        self.port = 0
        self.files = []

    @staticmethod
    def display_help() -> None:
        """
        Shows the help menu
        """
        print("\n==== LOBBIT HELP MENU ====\n"
              "\nBase commands:\n"
              "  set - Set the value of a required input\n"
              "  file - perform an action on a file or list of files\n"
              "  user - perform an action on a user object\n"
              "\nSet commands:\n"
              "  ip - set the IPv4 address of the remote server (REQUIRED)\n"
              "  port - set the port of the remote server (REQUIRED)\n"
              "\nFile commands:\n"
              "  add - add a file to the list of files to be uploaded\n"
              "  list - list the files you have added for upload\n"
              "  upload - upload the files you have added\n"
              "\nUser commands:\n"
              "  create - create a new user\n"
              "  update - update a password for an existing user\n"
              "  delete - delete an existing user\n"
              "\nExamples:\n"
              "  Set IPv4 address       : set ip 100.200.0.1\n"
              "  Add 2 files for upload : file add /path/to/file1 /another/path/to/file2\n"
              "  Change user password   : user update <username> <password>\n")

    @staticmethod
    def exit(interrupt=False) -> None:
        """
        Exits the REPL and returns the user to their terminal prompt

        Args:
            interrupt (bool) : states if KeyboardInterrupt quit the program
        """
        print("\nBye!") if interrupt else print("Bye!")
        sys.exit(1)

    @staticmethod
    def alert(message: str, status: int) -> None:
        """
        Displays the message to the user upon either successful
        execution of a command or when an error occurs. The statuses
        are:

        1: Successful command execution
        2: Error
        3: Bad input
        4: Incomplete command

        Args:
            message (str) : alert message to display
            status (int)  : indicates the level of alert
        """
        if status == 1:
            print(f"[+] Success: {message}")
        if status == 2:
            print(f"[-] Error: {message}")
        if status == 3:
            print(f"[-] Bad input: {message}")
        if status == 4:
            print(f"[*] Incomplete input: {message}")

    def run(self) -> None:
        """
        Starts the REPL and gets command line input from the
        user for processing
        """
        try:
            while self.cmd != "quit":
                self.cmd = input(self.prompt)
                if self.cmd == "":
                    continue
                self.verify_cmd_syntax()
            self.exit()
        except KeyboardInterrupt:
            self.exit(True)

    def verify_cmd_syntax(self) -> None:
        """
        Verifies that the base and sub commands provided by
        the user are valid
        """
        cmd_split = self.cmd.split(" ")
        len_cmds = len(cmd_split)
        if len_cmds == 1:
            self.handle_single_cmd()
            return
        if not self.is_base_cmd(cmd_split[0]) or not self.is_sub_cmd(cmd_split[1]):
            self.alert(f"unknown command '{self.cmd}'", 3)
            return
        else:
            if len(cmd_split) == 2:
                if cmd_split[0] == "file" and cmd_split[1] == "list":
                    self.handle_list()
                    return
                self.alert(f"'{self.cmd}'", 4)
                return
        self.parse_cmd(cmd_split)

    def parse_cmd(self, cmd_split: List) -> None:
        """
        Verifies a complete command to ensure the arguments
        passed in are valid. If the first two commands are valid
        then the correct handler method is called from the
        <self.cmd_map> to parse the commands arguments

        Args:
            cmd_split (List) : list of strings that make up a full
                               command
        """
        base = cmd_split[0]
        sub = cmd_split[1]
        self.args = cmd_split[2:]
        self.cmd_map.get(base).get(sub)()

    def handle_single_cmd(self) -> None:
        """
        Process a single command and display the appropriate
        output to the user
        """
        if self.cmd == "help":
            self.display_help()
        elif self.is_base_cmd(self.cmd):
            self.alert(f"'{self.cmd}'", 4)
        elif self.cmd == "quit":
            self.exit()
        else:
            self.alert(f"unknown command '{self.cmd}'", 3)

    def is_base_cmd(self, value: str) -> bool:
        """
        Checks to see if the value passed in is a base command and
        returns the command if it is, otherwise a bad input warning
        is sent to stdout

        Args:
            value (str) : the value to check
        Returns:
            bool: True if the value is a valid base command
        """
        return value in self.cmd_map.keys() or (value == "" or value == "help")

    def is_sub_cmd(self, value: str) -> bool:
        """
        Checks to see if the value passed in is a sub command and
        returns the sub command if it is, along with its parent command.
        Otherwise, a bad input warning is sent to stdout

        Args:
            value (str) : the value to check
        Returns:
            bool: True if the value is a valid sub command
        """
        for key in self.cmd_map:
            if value in self.cmd_map[key].keys():
                return True
        return False

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
    def valid_path(file_path: str) -> bool:
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
            return os.path.isfile(path)
        except TypeError:
            return False

    def handle_ip(self) -> None:
        """
        Process the set ip command
        """
        if len(self.args) > 1:
            self.alert("too many arguments", 3)
            return
        self.ip = self.args[0]
        if not self.valid_ip():
            self.ip = ""
            self.alert(f"invalid IP address '{self.args[0]}'", 2)
            return
        self.alert(f"IP address set to '{self.args[0]}'", 1)

    def handle_port(self) -> None:
        """
        Process the set port command
        """
        if len(self.args) > 1:
            self.alert("too many arguments", 3)
            return
        try:
            self.port = int(self.args[0])
            if not self.valid_port():
                self.port = 0
                self.alert(f"invalid port number '{self.args[0]}'", 2)
                return
            self.alert(f"Port number set to '{self.args[0]}'", 1)
        except ValueError:
            self.alert(f"invalid port number '{self.args[0]}'", 2)

    def handle_add(self) -> None:
        """
        Process the file add command
        """
        for arg in self.args:
            if not self.valid_path(arg):
                self.alert(f"invalid file path '{arg}'", 2)
                continue
            if os.path.isabs(arg):
                self.files.append(arg)
            else:
                self.files.append(f"{os.getcwd()}/{arg}")

    def handle_list(self) -> None:
        """
        Process the file list command
        """
        if not self.files:
            self.alert("file list is empty", 2)
            return
        for file in self.files:
            print(file)

    def handle_upload(self) -> None:
        """
        Process the file upload command
        """
        pass

    def handle_create(self) -> None:
        """
        Process the user create command
        """
        pass

    def handle_update(self) -> None:
        """
        Process the user update command
        """
        pass

    def handle_delete(self) -> None:
        """
        Process the user delete command
        """
        pass


def main() -> None:
    """
    Main function to run the Lobbit tool's interactive REPL
    in the client's terminal
    """
    repl = LobbitREPL()
    repl.run()


if __name__ == "__main__":
    main()
