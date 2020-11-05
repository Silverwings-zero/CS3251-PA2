'''
author: Wanli Qian
gtid: 903442597
Description: This program features the Server side of the simple tweet application
References: TCPClient.py and TCPServer.py from textbook slides
'''

from socket import *
import argparse


def main():
    '''
    Command Line Formatting:
    argument 0: the file
    argument 1: positional argument ServerPort indicate which port the server runs
    '''
    parser = argparse.ArgumentParser(description= 'minitweet server side')
    parser.add_argument('ServerPort', type=int)
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)

def run(args):
    try:
        #specifies server port according to input
        serverPort = int(args.ServerPort)
        #check whether server port is out of bounds
        if serverPort < 1000 or serverPort > 65535:
           raise ValueError("serverPort Value invalid")
        #define socket using ip4 and TCP
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.bind(("", serverPort))
        serverSocket.listen(1)
        print("ServerPort Starts at %s"%serverPort)
        buffer = ""
        usernameList = []
        while True:
            #Connect with Client and receive message from client
            connectionSocket, address = serverSocket.accept()
            fromClient = connectionSocket.recv(1024).decode()

            #check if the username already been taken
            print('The username from client is : ', fromClient)
            if fromClient in usernameList:
                failureMsg = "the username is invalid, already exists"
                print('current list is', usernameList)
                connectionSocket.send(failureMsg.encode())
            else:
                successMsg = "the username works, already added"
                usernameList.append(fromClient)
                print('current list is', usernameList)
                connectionSocket.send(successMsg.encode())

            # #Determine client modes from the first two characters in client message
            # #upload mode change the buffer to the client message and notify the client
            # if fromClient[0:2] == "-u":
            #     print('client upload mode, with upload message %s' %fromClient[2:])
            #     successMsg = "Upload Successful"
            #     #send message back to client
            #     connectionSocket.send(successMsg.encode())
            #     buffer = fromClient[2:]
            # #download mode sends the message to the client
            # if fromClient[0:2] == "-d":
            #     print('client download mode')
            #     #send message back to client
            #     connectionSocket.send(buffer.encode())
            # #close connection with client
            connectionSocket.close()
    except ValueError:
        print("Error Message: serverPort value is invalid")
        exit()


if __name__=="__main__":
	main()