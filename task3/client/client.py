import socket
import pickle
import os
import getpass
import base64
from Crypto.Cipher import AES
from Crypto import Random

HEADER = 4096
PORT = 9001
FORMAT = 'utf-8'
key = b'Sixteen byte key'

#SERVER should be set according to the ip address in which server is running, which is displayed when the server is started. Since its client file,this should be set accordingly before providing this script to the client.
SERVER = "172.19.0.2" 
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
            exit()
        else :
            iv = Random.new().read(AES.block_size)
            aes = AES.new(key, AES.MODE_CBC, iv)
            enc_iv = base64.b64encode(iv)
            file = open(msg, 'rb')
            while True:
                forEncData = file.read(HEADER)
                n = len(forEncData)
                if n == 0:
                    break
                elif n % 16 != 0:
                    forEncData += b' ' * (16 - n % 16)
                    pad_size = len(b' ' * (16 - n % 16))
                info = [enc_iv,pad_size]
                info_list = pickle.dumps(info)
                client.send(info_list)
                client.recv(16)
                encData = aes.encrypt(forEncData)
                client.sendall(encData) 
                print("File sent successfully.")
                

    else :
        print("No such file in current directory")
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
            exit()

    except UnicodeDecodeError :
        info_list = pickle.loads(info)
        enc_iv = info_list[0]
        iv = base64.b64decode(enc_iv)
        aes = AES.new(key, AES.MODE_CBC, iv)

        client.send('vector recvd'.encode(FORMAT))

        file_data = ''
        while True:
            partial = client.recv(HEADER)
            if len(partial) == 0:
                break
            file_data += (aes.decrypt(partial)).decode(FORMAT)
        
        pad_size = int(info_list[1])
        original_data = file_data[:-pad_size]
        file = open(msg, 'w')
        file.write(original_data)
        file.close()
        print("File recieved successfully!")

def delete(msg):
    sendf = pickle.dumps(["remove",msg])
    client.send(sendf)
    print(client.recv(HEADER).decode(FORMAT))

def view():
    sendf = pickle.dumps(["view"])
    client.send(sendf)
    msg = client.recv(HEADER)
    files_list = pickle.loads(msg)
    print("The files are :")
    for i in files_list:
        print(i)

def search(msg):
    sendf = pickle.dumps(["search",msg])
    client.send(sendf)
    info = client.recv(HEADER)
    print(info.decode(FORMAT))
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
    print("1. Upload file to the server")
    print("2. Download file from the server")
    print("3. Remove file from the server")
    print("4. View files in the server")
    print("5. Search for a file in the server")
    
    try :
        choice = int(input("Enter your choice(1,2,3) : "))
        while True:
            if choice == 1:
                filename = input("Enter the file name you want to upload(with extension): ")
                upload(filename)
                break
            elif choice == 2:
                filename = input("Enter the file name you want(with extension) : ")
                recv(filename)
                break
            elif choice == 3:
                filename = input("Enter the file name you want to delete(with extension) : ")
                delete(filename)
                break
            elif choice == 4:
                view()
                break
            elif choice == 5:
                filename = input("Enter the file name you want to delete(with extension) : ")
                search(filename)
            else :
                print("Wrong input for the choice. Enter integer 1,2 or 3.")
                client.send(pickle.dumps([""]))
                exit()
    
    except ValueError:
        print("Wrong input for the choice. Enter integer 1,2 or 3.")
        client.send(pickle.dumps([""]))
        exit()

