#!/bin/bash python

import argparse
import ipaddress
import os
import socket
import sys

from typing import Dict, List, Union


class LobbitClient:
    """
    Initialises a socket connection to the address and port
    passed in by the user and provides functions for checking
    and uploading files
    """

    def __init__(self, ip: str, port: int, files: List) -> None:
        """
        Constructor for the LobbitClient class

        Args:
            ip (str)     : remote IPv4 address
            port (int)   : remote port to connect to
            files (List) : list of files to upload to the server
        """
        self.ip = ip
        self.port = int(port)
        self.files = files
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer_size = 4096
        self.delimiter = "<DELIMITER>"

    def lobbit_connect(self) -> None:
        """
        Create the connection to the remote location
        """
        try:
            print(f"\n[+] Connecting to {self.ip}:{self.port}...")
            self.sock.connect((self.ip, self.port))
            print("[+] Connected successfully\n")
        except ConnectionRefusedError:
            print(f"\n[-] Failed to connect to {self.ip}:{self.port}. Check that the server application is running\n")
            sys.exit(2)
        except TimeoutError:
            print(f"\n[-] Failed to connect to {self.ip}:{self.port}. Check IP values and network settings\n")
            sys.exit(2)

    def lobbit_send(self) -> None:
        """
        Sends the file supplied by the user to the remote
        location using the socket instance
        """
        for file in self.files:
            self.sock.send(f"{file}{self.delimiter}{self.get_file_sizes()[file]}".encode())
            with open(file, "rb") as data:
                while True:
                    bytes_read = data.read(self.buffer_size)
                    if not bytes_read:
                        break
                    self.sock.sendall(bytes_read)
        self.sock.close()

    def get_file_sizes(self) -> Dict:
        """
        Gets the file size for each file in the list <self.files>
        and returns a dictionary of each file with its size
        """
        file_sizes_dict = dict()
        for file in self.files:
            file_sizes_dict[file] = os.path.getsize(file)
        return file_sizes_dict


def valid_ip(ip: str) -> Union[str, bool]:
    """
    Checks that the value of <ip> is a valid IPv4 address

    Args:
         ip (str) : the IPv4 address to validate
    Returns:
        str : the value of <ip> if a ValueError is not raised
    """
    try:
        return str(ipaddress.ip_address(ip))
    except ValueError:
        return False


def valid_port(port: int) -> bool:
    """
    Checks that the value of <port> is an integer from 1-65535

    Args:
        port (int) : the port number to validate
    Returns:
        bool : True if valid, False if not
    """
    try:
        return 1 <= int(port) <= 65535
    except TypeError:
        return False
    except ValueError:
        return False


def valid_path(file_path: str) -> bool:
    """
    Checks the system path passed in as <file_path> to ensure
    that a valid file object can be found at the path

    Args:
        file_path (str) : system path to check
    Returns:
        bool : True is path is a file, False if not
    """
    try:
        if os.path.isabs(file_path):
            return os.path.isfile(file_path)
        return os.path.isfile(f"{os.getcwd()}/{file_path}")
    except TypeError:
        return False


def get_parser() -> argparse.ArgumentParser:
    """
    Creates and returns an instance of argparse.ArgumentParser

    Returns:
        argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", dest="ip", help="The IP of the remote host")
    parser.add_argument("-p", "--port", dest="port", help="The network port on the remote host")
    parser.add_argument(
        "-f",
        "--files",
        dest="files",
        nargs="+",
        default=[],
        help="The file to be uploaded to the remote host")
    return parser


def check_parse_errors(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    """
    Checks the values in the <args> Namespace object and raises
    an Exception if an error is found

    Args:
        parser (argparse.ArgumentParser) : argument parser
        args (argparse.Namespace)        : args passed in by the user
    """
    if not valid_ip(args.ip):
        parser.error(f"\n\n[-] '{args.ip}' is an invalid IPv4 address\n")
    if not valid_port(args.port):
        parser.error(f"\n\n[-] '{args.port}' is an invalid port number\n")
    if not args.files:
        parser.error(f"\n\n[-] Provide a file or files to send\n")
    for file in args.files:
        if not valid_path(file):
            parser.error(f"\n\n[-] '{file}' is not a valid file path\n")


def get_args() -> argparse.Namespace:
    """
    Gets arguments from the command line to initialise values
    for the remote server IP address, remote server port number,
    and the files that will be sent to the remote location

    Returns:
        argparse.Namespace : arguments passed in by client
    """
    parser = get_parser()
    args = parser.parse_args()
    check_parse_errors(parser, args)
    return args


def main() -> None:
    """
    Main function for the lobbit client
    """
    args = get_args()
    client = LobbitClient(args.ip, args.port, args.files)
    client.lobbit_connect()
    client.lobbit_send()


if __name__ == "__main__":
    main()
