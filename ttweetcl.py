'''
author: Wanli Qian
gtid: 903442597
Description: This program features the client side of the simple tweet application, have upload and download functions
References: TCPClient.py and TCPServer.py from textbook slides
'''

from socket import *
import sys
import argparse


def main():
    '''
    Command Line Formatting:
    argument 0: the file
    argument 1: positional argument ServerIP the name of the Server in dotted format
    argument 2: positional argument ServerPort indicate which port the user wants to connect
    argument 3: positional argument userName indicate the userName that we take
    '''
    parser = argparse.ArgumentParser(description= 'minitweet client side')
    parser.add_argument('ServerIP', type = str)
    parser.add_argument('ServerPort', type = int)
    parser.add_argument('Username', type = str)

    #attaching function run
    parser.set_defaults(func=run)
    args = parser.parse_args()

    args.func(args)


def run(args):
    #check Server Ip formatting, raise exception if the input ip doesn't follow the standard format
    try:
        #print(args.ServerIP)
        IP = inet_aton(args.ServerIP)
        serverIP = str(args.ServerIP)
    except:
        print("error: server ip invalid, connection refused.")
        exit()

    try:
        #print(args.ServerPort)
        serverPort = int(args.ServerPort)
        #check serverPort value, raise error if server port is out of bound
        if serverPort < 1000 or serverPort > 65535:
           raise ValueError("error: server port invalid, connection refused.")
        

        #check user name only contains alphanumeric characters
        #print(args.Username.isalnum())
        if (not args.Username.isalnum()):
            raise ValueError("error: username has wrong format, connection refused.")

        message = "username " + args.Username

        #define socket using ip4 and TCP
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.settimeout(5)
        clientSocket.connect((serverIP, serverPort))
        #send the encoded upload string to server
        clientSocket.send(message.encode())
        #receive message from Server
        serverMsg = clientSocket.recv(1024).decode()

        print(serverMsg)
        
        #username invalid, exit
        if serverMsg == "the username is invalid, already exists":
            exit()

        #prompt command line
        while True:
            print("Command: ", end="")
            commandinput = input()
            #pass in username
            command = commandinput + " " + args.Username
            clientSocket.send(command.encode())
            msg = clientSocket.recv(1024).decode()
            print(msg)
            if commandinput == "getusers": 
                res = msg.strip('][').split(', ') 
                for i in range(len(res)):
                    #print("user number ", i, ": ", res[i], "\n")
                    print(res[i])
                res = None
                msg = None
            
            if msg == "close":
                break
        
        #close client socket
        clientSocket.close()
    except ConnectionRefusedError:
        print("Error Message: Server Not Found")
        exit()
    except timeout:
        print("Error Message: Session timeout")
        exit()
    except ValueError:
        print("Error Message: argument value is invalid")
        exit()
    except OSError:
        print("Error Message: Check the ServerIP, no route to host")

if __name__=="__main__":
	main()