#!/bin/bash python

import json
import os
import socket
import ssl
import sys

from _thread import start_new_thread
from threading import Lock
from typing import Tuple

lobbit_app = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../../")
sys.path.append(lobbit_app)

if lobbit_app in sys.path:
    from app.lobbit_util.buffer import Buffer


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
        self.thread_lock = Lock()
        self.context = self.get_ssl_context()

    @staticmethod
    def get_ssl_context() -> ssl.SSLContext:
        """
        Creates a default SSLContext object for socket encryption/decryption
        and loads the SSL certificate used for client authentication to the
        server

        Returns:
            SSLContext: the default context to wrap the socket
        """
        context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS)

        current_dir = os.path.abspath(os.path.dirname(__file__))
        with open(f"{current_dir}/../../config.json") as file:
            config = json.load(file)

        path = config['SERVER_CERT_PATH']
        exists, msg = LobbitServer.cert_exists(path)
        if exists:
            context.load_cert_chain(certfile=path, keyfile=path)
            return context
        else:
            print(msg)
            sys.exit(1)

    @staticmethod
    def cert_exists(path: str) -> Tuple[bool, str]:
        """
        Checks for the existence of a .pem certificate file at the location
        defined in config.json as SERVER_CERT_PATH

        Returns:
            bool: True if <cert_name>.pem exists, False is not
        """
        if not os.path.isfile(path):
            return False, "[-] File not found, check value of SERVER_CERT_PATH"
        suffix = path.split(".")[-1].lower()
        if suffix != "pem":
            return False, f"[-] Expected .pem certificate file type, found .{suffix} file"
        return True, ""

    def lobbit_listen(self) -> None:
        """
        Binds the ip and port to the socket instance
        held in <self.sock> then starts listening on
        that port
        """
        self.sock.bind((self.ip, self.port))
        self.sock.listen(10)
        print(f"[+] Server listening on {self.ip}:{self.port}...")

    def lobbit_accept(self) -> None:
        """
        Accepts incoming connections from the client
        """
        try:
            while True:
                self.sock = self.context.wrap_socket(self.sock, server_side=True)
                self.client_sock, address = self.sock.accept()
                self.thread_lock.acquire()
                print(f"[+] Client '{address[0]}:{address[1]}' accepted")
                start_new_thread(self.lobbit_receive, (address,))
        except KeyboardInterrupt:
            print("\r[+] Shutting down server... bye!\n")
            sys.exit(0)

    def lobbit_receive(self, connection: Tuple) -> None:
        """
        Receives the files that were sent from the server

        Args:
            connection (Tuple) : contains the IP and port of the client
        """
        buffer = Buffer(self.client_sock)
        while True:
            file_name = buffer.get_utf8().split('/')[-1]
            if not file_name:
                self.thread_lock.release()
                break
            print(f"[+] File name: {file_name}")
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
        print(f"[+] Closing connection '{connection[0]}:{connection[1]}'...")
        print(f"[+] Server listening on {self.ip}:{self.port}...")
        self.client_sock.close()


def main() -> None:
    """
    Main function of the Lobbit server application
    """
    try:
        current_dir = os.path.abspath(os.path.dirname(__file__))
        with open(f"{current_dir}/../../config.json") as file:
            config = json.load(file)
        server = LobbitServer(config["HOST"], config["PORT"], config["UPLOAD_PATH"])
        server.lobbit_listen()
        server.lobbit_accept()
    except KeyboardInterrupt:
        print("\r[+] Shutting down server... bye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
