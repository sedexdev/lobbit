import os
import socket

from app.lobbit_util.buffer import Buffer
from typing import List


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

    def lobbit_connect(self) -> bool:
        """
        Create the connection to the remote location

        Returns:
            bool : True if connection was successful, False if not
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print(f"[+] Connecting to {self.ip}:{self.port}...")
            self.sock.connect((self.ip, self.port))
            print("[+] Connected successfully\n")
            return True
        except ConnectionRefusedError:
            print(f"[-] Connection '{self.ip}:{self.port}' failed. Check IP/port and that server app is running...")
            return False
        except TimeoutError:
            print(f"[-] Connection '{self.ip}:{self.port}' failed. Check IP/port and that server app is running...")
            return False

    def lobbit_send(self) -> None:
        """
        Sends the file supplied by the user to the remote
        location using the socket instance
        """
        buffer = Buffer(self.sock)
        for file in self.files:
            print(f"[+] Sending '{file}'...")
            buffer.put_utf8(file)
            file_size = os.path.getsize(file)
            buffer.put_utf8(str(file_size))
            with open(file, 'rb') as f:
                buffer.put_bytes(f.read())
            print("[+] File sent\n")
