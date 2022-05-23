#!/usr/bin/bash python3

import sys

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
        self.prompt = "lobbit> "
        self.context = "base"
        self.help = "help"
        self.quit = "quit"
        self.base_commands = ["set", "file", "user"]
        self.set_subcmds = ["ip", "port"]
        self.file_subcmds = ["add", "get", "remove", "move", "list", "upload"]
        self.user_subcmds = ["create", "update", "delete"]
        self.cmd = None

    def run(self) -> None:
        """
        Starts the REPL and gets command line input from the
        user for processing
        """
        try:
            while self.cmd != self.quit:
                self.cmd = input(self.prompt)
                self.parse_cmd()
            self.exit()
        except KeyboardInterrupt:
            self.exit()

    def exit(self) -> None:
        """
        Exits the REPL and returns the user to their terminal prompt
        """
        print("\nBye!")
        sys.exit(1)

    def parse_cmd(self) -> None:
        """
        Parses input from the user
        """
        pass

    def alert(self, message: str, status: int) -> None:
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
            self.display_help()

    def display_help(self) -> None:
        """
        Shows the help menu based on the current context
        """
        if self.context == "base":
            print("\nBase commands:"
                  "set - Set the value of a required input"
                  "file - perform an action on a file"
                  "user - perform an action on a user object")
        if self.context == "set":
            print("\nSet commands:"
                  "ip - set the IPv4 address of the remote server"
                  "port - set the port of the remote server")
        if self.context == "file":
            print("\nFile commands:"
                  "add - add a file to the list of files to be uploaded"
                  "get - get a single file from the remote server"
                  "remove - delete a file from the remote server"
                  "list - list the files you have added for upload"
                  "move - move a file on the remote server"
                  "upload - upload the files you have added")
        if self.context == "user":
            print("\nUser commands:"
                  "create - create a new user"
                  "update - update a username or password for an existing user"
                  "delete - delete an existing user")


def main() -> None:
    """
    Main function to run the Lobbit tool's interactive REPL
    in the client's terminal
    """
    repl = LobbitREPL()
    repl.run()


if __name__ == "__main__":
    main()
