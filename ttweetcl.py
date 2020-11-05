from socket import *
import sys

try:
    if len(sys.argv) != 5 and len(sys.argv) != 4:
        raise Exception
    if sys.argv[1] == "-u" and len(sys.argv) == 4:
        raise Exception
    if sys.argv[1] == "-d" and len(sys.argv) == 5:
        raise Exception
except Exception:
    print("Incorrect amount of arguments")
    exit()


mode = sys.argv[1]
serverIP = sys.argv[2]
try:
    serverPort = int(sys.argv[3])
    if serverPort < 13000 or serverPort > 14000:
        raise Exception
except Exception:
    print("Error: Incorrect port number format")
    exit()

try:
    ip = inet_aton(serverIP)
    ip = str(serverIP)
except:
    print("Error: Invalid serverIP")
    exit()

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.settimeout(1)

try:
    clientSocket.connect((serverIP, serverPort))
except Exception:
    print("Error Message: Server Not Found")
    exit()

if mode == "-u":
    message = sys.argv[4]
    try:
        if len(message) > 150 or len(message) <= 0:
            raise Exception
    except Exception:
        print("Message is longer than 150 characters or has 0 characters")
    else:   
        info = mode + message
        clientSocket.send(info.encode())
        serv_response = clientSocket.recv(1024).decode()
        print(serv_response)
elif mode =="-d":
    clientSocket.send(mode.encode())
    serv_response = clientSocket.recv(1024).decode()
    print(serv_response)

clientSocket.close()