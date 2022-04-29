#!/bin/bash python

import argparse
import ipaddress
import os
import socket
from typing import Union


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
        bool : True is path exists, False if not
    """
    try:
        return os.path.isfile(file_path)
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
    parser.add_argument("-f", "--file", dest="file", help="The file to be uploaded to the remote host")
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
    if not valid_path(args.file):
        parser.error(f"\n\n[-] '{args.file}' is not a valid file path\n")


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
    print(args)


if __name__ == "__main__":
    main()
