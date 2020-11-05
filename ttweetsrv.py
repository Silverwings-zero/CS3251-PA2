from socket import *
import sys


try:
    if len(sys.argv) != 2:
        raise Exception
except:
    print("Number of input arguments is incorrect")
    exit()

try:
    serverPort = int(sys.argv[1])
    if serverPort < 13000 or serverPort > 14000:
        raise Exception
except Exception:
    print("Error: Invalid port number format")
    exit()
serverScoket = socket(AF_INET, SOCK_STREAM)
serverScoket.bind(("127.0.0.1", serverPort))
serverScoket.listen(1)

sentence = ""

while True:
    connectionSocket, address = serverScoket.accept()
    info = connectionSocket.recv(1024).decode()
    if info[0:2] == "-u":
        sentence = info[2:]
        connectionSocket.send("Upload Successful".encode())
    elif info[0:2] == "-d":
        connectionSocket.send(sentence.encode())

    connectionSocket.close()