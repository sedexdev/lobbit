# lobbit: a tool for transferring files to a remote location

The lobbit tool is used for the secure transfer of files in a single direction; from client to 
server. The tool requires that the server application is running on the remote device to allow incoming
connections. Security is provided through username/password credentials, using SHA256 hashing, which are
transferred to the server using AES/RSA public key cryptography. The server only sends event alerts back
to the client, with connection details being logged for auditing purposes.

# Usage

# Options

# Events

# License

<a href="https://github.com/sedexdev/lobbit/blob/main/LICENSE">M.I.T</a>
