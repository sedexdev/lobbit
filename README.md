# Lobbit: A file transfer tool

[![Test](https://github.com/sedexdev/lobbit/actions/workflows/test.yml/badge.svg)](https://github.com/sedexdev/lobbit/actions/workflows/test.yml)

The lobbit tool is used for the secure transfer of files in a single direction.

Lobbit can be used to send data to a location on your local machine or over the wire to a remote computer. It follows a classic client / server architecture and provides a REPL CLI for managing transfers. Security is provided through authentication using a self-signed SSL certificate.

# 📦 Installation

## Prerequisites

```bash
Python >= 3.12
```

## Get the code

```bash
git clone https://github.com/sedexdev/lobbit.git
```

# ⚙️ Configuration

- Create a directory called `certs` under the _root directory_
- Generate a self-signed SSL certificate in this directory

```bash
mkdir certs && cd certs
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365 -nodes

# Add values appropriate for your needs
# For local data transfer set the CN to 'localhost'
```

- Create a file called `config.json` under the _root directory_
- Paste in the below config

```bash
vim config.json
# paste in the following values
{
  "HOST": "localhost",
  "PORT": 8443,
  "UPLOAD_PATH": "/path/to/uploads",
  "PUBLIC_CERT_PATH": "./certs/cert.pem",
  "PRIVATE_CERT_PATH": "./certs/key.pem"
}
```

# 🛠️ Usage

## Running Lobbit

- Running the client REPL CLI and the server

```bash
# Open 2 terminal sessions - one for the client and another for the server

# client
cd lobbit/app/lobbit_client
python3 repl.py

# server
cd lobbit/app/lobbit_server
python3 server.py
```

## Lobbit Commands

- Within the REPL the following commands are available:

**Base commands**

- `set` - Set the value of a required network parameter
- `file` - perform an action on a file or list of files
- `use` - use either 'hostname' or 'ip' for the remote connection
- `net` - display the current remote network parameters

**Set commands**

- `ip {IP_ADDRESS}` - set the IPv4 address of the remote server (REQUIRED)
- `port {PORT_NUMBER}` - set the port of the remote server (REQUIRED)

**File commands**

- `add {FILE_PATHS}` - add one or more file paths to the list of files to be uploaded
- `list` - list the files you have added for upload
- `remove {INDEXES}` - remove a file from the upload list
- `upload` - upload the files you have added

**Use commands**

- `hostname` - use a hostname for the remote connection
- `ip` - use an IP address for the remote connection

**Examples**

- Set IPv4 address : `set ip 100.200.0.1`
- Add 2 files for upload : `file add /path/to/file1 /another/path/to/file2`
- Remove added files at indexes 1 and 3 : `file remove 1 3`
- Use hostname instead of IP to connect : `use hostname`
- Set hostname : `set hostname localhost`

### Exiting the tool

- Use Ctrl+C to quit the REPL or the stop the server

# 📂 Project Structure

```
lobbit/
│
├── .github/          # GitHub workflows and issue templates
├── app/              # Source files
├── tests/            # Unit tests
├── .gitignore        # Ignore file for Git
├── LICENSE           # MIT OSS license
└── README.md         # This README.md file
```

# 🧪 Running Tests

```bash
# use the unittest module to run all tests
cd tests
python3 -m unittest -b tests/*.py
```

# 🐛 Reporting Issues

Found a bug or need a feature? Open an issue [here](https://github.com/sedexdev/lobbit/issues).

# 🧑‍💻 Authors

**Andrew Macmillan** – [@sedexdev](https://github.com/sedexdev)

# 📜 License

This project is licensed under the MIT License - see the [M.I.T](https://github.com/sedexdev/lobbit/blob/main/LICENSE) file for details.
