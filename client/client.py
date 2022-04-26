import socket
import pickle
import os
import getpass
import base64
from Crypto.Cipher import AES
from Crypto import Random

HEADER = 64*4096
PORT = 9001
FORMAT = 'utf-8'
key = b'B?E(H+MbPeShVmYq3t6w9z$C&F)J@NcR'

#SERVER should be set according to the ip address in which server is running, which is displayed when the server is started. Since its client file,this should be set accordingly before providing this script to the client.
SERVER = "127.0.0.1" 
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def upload(msg):
    if os.path.exists(msg):
        sendf = pickle.dumps(["upload", msg])
        client.send(sendf)
        message = client.recv(HEADER).decode(FORMAT)
        if message == "File already exists.":
            print(message)

        else :
            iv = Random.new().read(AES.block_size)
            aes = AES.new(key, AES.MODE_CFB, iv)
            enc_iv = base64.b64encode(iv)
            file = open(msg, 'rb')
        
            forEncData = file.read(HEADER)
            info = [enc_iv,len(forEncData)]
            print(info)
            info_list = pickle.dumps(info)
            client.send(info_list)
            client.recv(16)
            encData = aes.encrypt(forEncData)
            client.sendall(encData) 
            print(client.recv(HEADER).decode(FORMAT))
                

    else :
        print("No such file in current directory.")
        sendf = pickle.dumps([""])
        client.send(sendf)


def recv(msg):
    sendf = pickle.dumps(["download",msg])
    client.send(sendf)
    info = client.recv(HEADER)
    
    try :
        if info.decode(FORMAT) == "File not found.":
            print("File not found.")
            client.send('no file'.encode(FORMAT))

    except UnicodeDecodeError :
        info_list = pickle.loads(info)
        enc_iv = info_list[0]
        iv = base64.b64decode(enc_iv)
        aes = AES.new(key, AES.MODE_CFB, iv)

        client.send('vector recvd'.encode(FORMAT))

        data = client.recv(HEADER)
        file_data = aes.decrypt(data)
        
        file = open(msg, 'wb')
        file.write(file_data)
        file.close()
        client.send("File recieved successfully.".encode(FORMAT))
        print("File recieved successfully!")

def delete(msg):
    sendf = pickle.dumps(["remove",msg])
    client.send(sendf)
    print(client.recv(HEADER).decode(FORMAT))

def view():
    sendf = pickle.dumps(["view"])
    client.send(sendf)
    files_list = client.recv(HEADER).decode(FORMAT)
    print("The files are :")
    print(files_list)

def search(msg):
    sendf = pickle.dumps(["search",msg])
    client.send(sendf)
    info = client.recv(HEADER)
    print(info.decode(FORMAT))

def disconnect():
    sendf = pickle.dumps(["disconnect"])
    client.send(sendf)
    msg = client.recv(HEADER).decode(FORMAT)
    print(msg)
    exit()

# getpass.getuser() can be used to detect user automatically 
uname = input("Enter your AlphaQ username : ")
passw = getpass.getpass()

#Encoding credentials of the user
uname = base64.b64encode(f"{uname}".encode())
passw = base64.b64encode(f"{passw}".encode())
cred = [uname,passw]

credentials = pickle.dumps(cred)

client.send(credentials)

file_data = client.recv(HEADER)
if file_data.decode(FORMAT) == "Invalid Credentials":
        print("Invalid Credentials.")
        exit()
else :
    
    while True:
        print("1. Upload file to the server")
        print("2. Download file from the server")
        print("3. Remove file from the server")
        print("4. View files in the server")
        print("5. Search for a file in the server")
        print("6. Disconnect from the server")
        try :
            choice = int(input("Enter your choice : "))
            if choice == 1:
                filename = input("Enter the file name you want to upload(with extension): ")
                upload(filename)
            elif choice == 2:
                filename = input("Enter the file name you want(with extension) : ")
                recv(filename)
            elif choice == 3:
                filename = input("Enter the file name you want to delete(with extension) : ")
                delete(filename)
            elif choice == 4:
                view()
            elif choice == 5:
                filename = input("Enter the file name you want to delete(with extension) : ")
                search(filename)
            elif choice == 6:
                disconnect()
            else :
                print("Wrong input for the choice.")
                client.send(pickle.dumps([""]))
            print()
            print("-----------------------")
        
        except ValueError:
            print("Wrong input for the choice")
            client.send(pickle.dumps([""]))
            print()
            print("-----------------------")

