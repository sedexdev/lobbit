from socket import socket
from typing import Union


class Buffer:
    """
    Defines a test_data buffer that can be used to receive
    information over an instance of <socket.socket>
    """

    def __init__(self, sock: socket) -> None:
        """
        Buffer class constructor

        Args:
            sock (socket) : socket instance for the buffer
        """
        self.sock = sock
        self.buffer = b''

    def get_bytes(self, len_bytes: int) -> bytes:
        """
        Read len_bytes from the connection into the buffer

        Args:
            len_bytes (int) : exact number of bytes to buffer
        Returns:
            bytes : byte test_data sent over the socket
        """
        while len(self.buffer) < len_bytes:
            data = self.sock.recv(1024)
            if not data:
                data = self.buffer
                self.buffer = b''
                return data
            self.buffer += data
        # split message bytes from the buffer
        data, self.buffer = self.buffer[:len_bytes], self.buffer[len_bytes:]
        return data

    def put_bytes(self, data: bytes) -> None:
        """
        Send buffered test_data over the socket

        Args:
            data (bytes) : test_data being sent over the socket
        """
        self.sock.sendall(data)

    def get_utf8(self) -> Union[str, bytes]:
        """
        Reads a null terminated UTF-8 string and decodes it

        Returns:
            Union[str, bytes] : empty string or decoded bytes
        """
        while b'\x00' not in self.buffer:
            data = self.sock.recv(1024)
            if not data:
                return ''
            self.buffer += data
        # split the string off from the buffer
        data, _, self.buffer = self.buffer.partition(b'\x00')
        return data.decode()

    def put_utf8(self, data: str) -> None:
        """
        Send buffered UTF-8 data over the socket

        Args:
            data (str) : data being sent over the socket
        """
        if '\x00' in data:
            raise ValueError("string contains delimiter 'null'")
        self.sock.sendall(data.encode() + b'\x00')
