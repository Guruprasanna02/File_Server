# File Server

File Server is an easy-to-use command-line application to transfer files securely utilizing AES-256 encryption on a dockerized multi-threaded server within an organization.

## Setup

To setup the server:
```bash
docker-compose up --build -d
```

Application can be accessed from client side by running the ```client.py script```
```bash
cd ./client
python client.py
```