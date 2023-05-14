import json
import os
import socket
import ssl

from app.lobbit_util.buffer import Buffer
from typing import List, Tuple


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
        self.host = ip
        self.port = port
        self.files = files
        self.sock = None
        self.context = ssl.create_default_context()

    @staticmethod
    def cert_exists(path: str) -> Tuple[bool, str]:
        """
        Checks for the existence of a .pem certificate file at the location
        defined in config.json as SERVER_CERT_PATH

        Returns:
            bool: True if <cert_name>.pem exists, False is not
        """
        if not os.path.isfile(path):
            return False, "[-] File not found, check value of CLIENT_CERT_PATH"
        suffix = path.split(".")[-1].lower()
        if suffix != "pem":
            return False, f"[-] Expected .pem certificate file, found .{suffix}"
        return True, ""

    def lobbit_connect(self) -> bool:
        """
        Create the connection to the remote location

        Returns:
            bool : True if connection was successful, False if not
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print(f"[+] Connecting to {self.host}:{self.port}...")
            self.sock = self.context.wrap_socket(self.sock, server_hostname=self.host)

            current_dir = os.path.abspath(os.path.dirname(__file__))
            with open(f"{current_dir}/../../config.json") as file:
                config = json.load(file)
                
            path = config['CLIENT_CERT_PATH']
            exists, msg = LobbitClient.cert_exists(path)
            if exists:
                self.context.load_verify_locations(config['CLIENT_CERT_PATH'])
                self.sock.connect((self.host, self.port))
                print("[+] Connected successfully\n")
                return True
            else:
                print(msg)
        except ConnectionRefusedError as e:
            print(e)
            print(f"[-] Connection '{self.host}:{self.port}' failed. Connection refused...")
            return False
        except TimeoutError:
            print(f"[-] Connection '{self.host}:{self.port}' failed. Connection timeout...")
            return False
        except Exception as e:
            print(f"[-] Exception caught: {e}")
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
