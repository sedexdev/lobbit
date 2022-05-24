#!/usr/bin/bash python3

import sys

# from lobbit.client import LobbitClient


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
        self.prompt = "lobbit> "
        self.set_subcmds = ["ip", "port"]
        self.file_subcmds = ["add", "get", "remove", "move", "list", "upload"]
        self.user_subcmds = ["create", "update", "delete"]
        self.cmd_map = {
            "reset": [],
            "set": self.set_subcmds,
            "file": self.file_subcmds,
            "user": self.user_subcmds
        }
        self.cmd = None

    @staticmethod
    def display_help() -> None:
        """
        Shows the help menu
        """
        print("\nBase commands:\n"
              "set - Set the value of a required input\n"
              "file - perform an action on a file\n"
              "user - perform an action on a user object\n"
              "\nSet commands:\n"
              "ip - set the IPv4 address of the remote server\n"
              "port - set the port of the remote server\n"
              "\nFile commands:\n"
              "add - add a file to the list of files to be uploaded\n"
              "get - get a single file from the remote server\n"
              "remove - delete a file from the remote server\n"
              "list - list the files you have added for upload\n"
              "move - move a file on the remote server\n"
              "upload - upload the files you have added\n"
              "\nUser commands:\n"
              "create - create a new user\n"
              "update - update a username or password for an existing user\n"
              "delete - delete an existing user\n")

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

        1: success
        2: error
        3: bad input

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
                self.parse_cmd()
            self.exit()
        except KeyboardInterrupt:
            self.exit(True)

    def parse_cmd(self) -> None:
        """
        Parses input from the user
        """
        cmds = self.cmd.split(" ")
        len_cmds = len(cmds)
        if len_cmds == 1:
            self.cmd = cmds[0]
            return
        i = 0
        while i < len_cmds:
            if i == 0:
                if not cmds[i] == self.is_base_cmd(cmds[i]):
                    self.alert(f"unknown command '{cmds[i]}'", 3)
            i += 1

    def is_base_cmd(self, value: str) -> str:
        """
        Checks to see if the value passed in is a base command and
        returns the command if it is, otherwise a bad input warning
        is sent to stdout

        Args:
            value (str) : the value to check
        """
        if value in self.cmd_map.keys() or value == "":
            return value
        self.alert(f"unknown command '{value}'", 3)

    def is_sub_cmd(self, value: str) -> tuple:
        """
        Checks to see if the value passed in is a sub command and
        returns the sub command if it is, along with its parent command.
        Otherwise, a bad input warning is sent to stdout

        Args:
            value (str) : the value to check
        Returns:
            tuple: base command, sub command
        """
        for key in self.cmd_map:
            if value in self.cmd_map[key]:
                return key, value
        self.alert(f"unknown command '{value}'", 3)

    def set_value(self, value: str, sub_cmd: str) -> None:
        """
        Sets either the IPv4 address or the port number

        Args:
            value (str)   : the value to set
            sub_cmd (str) : command that dictates which to set
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
