# lobbit: a tool for transferring files to a remote location

SSL self-signed cert: openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365 -nodes

The lobbit tool is used for the secure transfer of files in a single direction; from client to
server. The tool requires that the server application is running on the remote device to allow incoming
connections. Security is provided through authentication using a self-signed SSL certificate.

# Usage

<b>Available commands</b></br>
<code>set</code> - Set the value of a required network parameter</br>
<code>file</code> - perform an action on a file or list of files</br>
<code>use</code> - use either 'hostname' or 'ip' for the remote connection</br>
<code>net</code> - display the current remote network parameters</br>

<b>Sub-commands</b></br>
Set</br>
<code>ip</code> [IP_ADDRESS] - set the IPv4 address of the remote server (REQUIRED)</br>
<code>port</code> [PORT_NUMBER] - set the port of the remote server (REQUIRED)</br>

File</br>
<code>add</code> [FILE_PATHS] - add one or more file paths to the list of files to be uploaded</br>
<code>list</code> - list the files you have added for upload</br>
<code>remove</code> [INDEXES] - remove a file from the upload list</br>
<code>upload</code> - upload the files you have added</br>

Use</br>
<code>hostname</code> - use a hostname for the remote connection</br>
<code>ip</code> - use an IP address for the remote connection</br>

<b>Examples</b></br>
Set IPv4 address : <code>set ip 10.0.0.1</code></br>
Add 2 files for upload : <code>file add /path/to/file1 /another/path/to/file2</code></br>
Remove added files at indexes 1 and 3 : <code>file remove 1 3</code></br>
Use hostname instead of IP to connect : <code>use hostname</code></br>
Set hostname : <code>set hostname {hostname}</code></br>

# License

<a href="https://github.com/sedexdev/lobbit/blob/main/LICENSE">M.I.T</a>
