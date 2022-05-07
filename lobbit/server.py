#!/bin/bash python

import json
import os
import socket
import sys


class LobbitServer:
    """
    Initialises a socket that waits for incoming
    connections from the client application
    """

    def __init__(self, ip: str, port: int) -> None:
        """
        Constructor for the LobbitServer class

        Args:
            ip (str)   : local IPv4 address
            port (int) : local port for clients to connect to
        """
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock = None
        self.buffer_size = 4096
        self.delimiter = "<DELIMITER>"

    def lobbit_listen(self) -> None:
        """
        Binds the ip and port to the socket instance
        held in <self.sock> then starts listening on
        that port
        """
        self.sock.bind((self.ip, self.port))
        self.sock.listen(5)
        print(f"\n[+] Server listening on {self.ip}:{self.port}...")

    def lobbit_accept(self) -> None:
        """
        Accepts incoming connections from the client
        """
        self.client_sock, address = self.sock.accept()
        print(f"[+] Client {address} accepted\n")

    def lobbit_receive(self) -> None:
        """
        Receives the files that were sent from the server
        """
        if isinstance(self.client_sock, socket.socket):
            received = self.client_sock.recv(self.buffer_size).decode()
            file_name, file_size = received.split(self.delimiter)
            file_name = os.path.basename(file_name)
            file_size = int(file_size)
            with open(file_name, "wb") as data:
                print(f"[+] Writing {int(file_size)} bytes of data to '{file_name}'...")
                while True:
                    bytes_read = self.client_sock.recv(self.buffer_size)
                    if not bytes_read:
                        break
                    data.write(bytes_read)
                print(f"[+] '{file_name}' written successfully\n")
            self.client_sock.close()
            self.sock.close()
        else:
            print("\n[-] Socket not configured to accept connections, exiting")
            sys.exit(2)


def main() -> None:
    """
    Main function of the Lobbit server application
    """
    with open(f"{os.path.abspath(os.path.dirname(__file__))}/../config.json") as file:
        config = json.load(file)
    server = LobbitServer(config["SERVER_HOST"], config["SERVER_PORT"])
    server.lobbit_listen()
    server.lobbit_accept()
    server.lobbit_receive()


if __name__ == "__main__":
    main()
