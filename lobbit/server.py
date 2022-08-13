#!/bin/bash python

import json
import os
import socket

from lobbit.buffer import Buffer


class LobbitServer:
    """
    Initialises a socket that waits for incoming
    connections from the client application
    """

    def __init__(self, ip: str, port: int, upload_path: str) -> None:
        """
        Constructor for the LobbitServer class

        Args:
            ip (str)          : local IPv4 address
            port (int)        : local port for clients to connect to
            upload_path (str) : upload destination
        """
        self.ip = ip
        self.port = port
        self.upload_path = upload_path
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock = None

    def lobbit_listen(self) -> None:
        """
        Binds the ip and port to the socket instance
        held in <self.sock> then starts listening on
        that port
        """
        self.sock.bind((self.ip, self.port))
        self.sock.listen(10)
        print(f"\n[+] Server listening on {self.ip}:{self.port}...")

    def lobbit_accept(self) -> None:
        """
        Accepts incoming connections from the client
        """
        self.client_sock, address = self.sock.accept()
        print(f"[+] Client {address} accepted")

    def lobbit_receive(self) -> None:
        """
        Receives the files that were sent from the server
        """
        buffer = Buffer(self.client_sock)
        while True:
            file_name = buffer.get_utf8().split('/')[-1]
            if not file_name:
                break
            print(f"\n[+] File name: {file_name}")
            file_size = int(buffer.get_utf8())
            print(f"[+] File size: {file_size}MB")
            with open(f"{self.upload_path}{file_name}", 'wb') as f:
                remaining = file_size
                while remaining:
                    chunk_size = 4096 if remaining >= 4096 else remaining
                    chunk = buffer.get_bytes(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    remaining -= len(chunk)
                if remaining:
                    print(f"[-] File incomplete, missing {remaining} bytes")
                else:
                    print(f"[+] File '{file_name}' received successfully")
        print("\n[+] Closing connection...\n")
        self.client_sock.close()


def main() -> None:
    """
    Main function of the Lobbit server application
    """
    with open(f"{os.path.abspath(os.path.dirname(__file__))}/../config.json") as file:
        config = json.load(file)
    server = LobbitServer(config["SERVER_HOST"], config["SERVER_PORT"], config["UPLOAD_PATH"])
    server.lobbit_listen()
    server.lobbit_accept()
    server.lobbit_receive()


if __name__ == "__main__":
    main()
