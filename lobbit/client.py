import os
import socket
import sys
import time

from typing import Dict, List


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
        self.port = port
        self.files = files
        self.sock = None
        self.buffer_size = 4096
        self.delimiter = "<DELIMITER>"

    def lobbit_connect(self) -> None:
        """
        Create the connection to the remote location
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            file_info = f"{file}{self.delimiter}{self.get_file_sizes()[file]}".encode()
            self.sock.send(file_info)
            time.sleep(1)
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

