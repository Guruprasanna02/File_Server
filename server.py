import socket
import threading
import pickle
import mysql.connector
import os
from os import walk
import base64
from Crypto.Cipher import AES
from Crypto import Random

# header size can be varied manually according to the maximum size of the file to be transferred or a while loop can be used in case there is no restriction
HEADER = 64*4096
PORT = 9001
SERVER = "0.0.0.0"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
key = b'B?E(H+MbPeShVmYq3t6w9z$C&F)J@NcR'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

#Enabling authentication of users
def auth(uname,passw):
    mydb = mysql.connector.connect(
        host="db", port="3306", user="root", passwd="password", database="AlphaQMoM")
    mycursor = mydb.cursor()
    mycursor.execute(
        f"Select * from allUsers where user='{uname}' AND password='{passw}'")
    myresult = mycursor.fetchall()
    x = len(myresult)
    return x

def upload(conn,addr,domain,filename):
    if os.path.exists(f"./{domain}/{filename}"):
        conn.send("File already exists.".encode(FORMAT))
        print(addr,": File already exists.")
    else :
        conn.send("proceed".encode(FORMAT))
        info = conn.recv(HEADER)

        info_list = pickle.loads(info)
        enc_iv = info_list[0]
        iv = base64.b64decode(enc_iv)
        aes = AES.new(key, AES.MODE_CFB, iv)

        conn.send('vector recvd'.encode(FORMAT))

        data = conn.recv(HEADER)
        file_data = aes.decrypt(data)
        
        file = open(f"./{domain}/{filename}", 'wb')
        file.write(file_data)
        file.close()
        conn.send("File uploaded successfully.".encode(FORMAT))
        print(addr,": File uploaded successfully.")

def download(conn,addr,domain,filename):
    if os.path.exists(f"./{domain}/{filename}"):
        iv = Random.new().read(AES.block_size)
        aes = AES.new(key, AES.MODE_CFB, iv)
        enc_iv = base64.b64encode(iv)
        
        file = open(f"./{domain}/{filename}", 'rb')
        forEncData = file.read(HEADER)
        info = [enc_iv,len(forEncData)]
        info_list = pickle.dumps(info)
        conn.send(info_list)
        conn.recv(16)
        encData = aes.encrypt(forEncData)
        conn.sendall(encData) 
        
        print(addr, conn.recv(HEADER).decode(FORMAT))
    else :
        conn.send("File not found.".encode(FORMAT))
        print(addr,": File not found.")

def remove(conn,addr,domain,filename):
    if os.path.exists(f"./{domain}/{filename}"):
        os.remove(f"./{domain}/{filename}")
        conn.send("File removed successfully.".encode(FORMAT))
        print(addr,": File removed successfully!")
    else :
        conn.send("File not found.".encode(FORMAT))
        print(addr,": File not found.")

def view(conn,addr,domain):
    f = []
    for (dirpath, dirnames, filenames) in walk(f"./{domain}/"):
        f.extend(filenames)
        break
    file_list = ''
    for i in f:
        file_list += f"{i}\n"
    conn.send(file_list.encode(FORMAT))
    print(addr,": Files sent successfully")

def search(conn,addr,domain,filename):
    if os.path.exists(f"./{domain}/{filename}"):
        conn.send("File exists.".encode(FORMAT))
        print(addr,"File exists.")
    else:
        conn.send("File does not exist.".encode(FORMAT))
        print(addr,"File does not exist.")

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    msgs = []
    connected = True
    while connected:
        msg = conn.recv(HEADER)
        msgs.append(msg)
        if len(msgs) == 1:
            cred = pickle.loads(msg)
            uname1 = base64.b64decode(cred[0]).decode()
            passw1 = base64.b64decode(cred[1]).decode()
            cred = [uname1,passw1]
            result = auth(cred[0],cred[1])
            if result == 1:
                uname = cred[0]
                if uname[0:6] == "sysAd_":
                    domain = "sysAd"
                    conn.send("welcome".encode(FORMAT))
                elif uname[0:7] == "webDev_":
                    domain = "webDev"
                    conn.send("welcome".encode(FORMAT))
                elif uname[0:7] == "appDev_":
                    domain = "appDev"
                    conn.send("welcome".encode(FORMAT))
            else :
                conn.send("Invalid Credentials".encode(FORMAT))
                print(addr,"Invalid User.")
                connected = False
                print(addr,"[Connection Closed]")
                break
        if len(msgs) != 1:
            option = pickle.loads(msg)
            if option[0] == "download":
                download(conn,addr,domain,option[1])

            elif option[0] == "upload":
                upload(conn,addr,domain,option[1])
            
            elif option[0] == "remove":
                remove(conn,addr,domain,option[1])
                
            elif option[0] == "view":
                view(conn,addr,domain)
                
            elif option[0] == "search":
                search(conn,addr,domain,option[1])
                
            elif option[0] == "disconnect":
                conn.send("Successfully disconnected from the server.".encode(FORMAT))
                conn.close()
                connected = False
                print(addr, "[Connection Closed]")
                break
            else :
                print(addr,"Wrong input.")
                

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] Server is starting...")
start()

