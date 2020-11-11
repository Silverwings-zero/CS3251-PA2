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
    parser.add_argument('ServerIP')
    parser.add_argument('ServerPort')
    parser.add_argument('Username')

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
           raise ValueError()
    except ValueError:
        print("error: server port invalid, connection refused.")
        exit()
    

    #check user name only contains alphanumeric characters
    #print(args.Username.isalnum())
    try:
        if (not args.Username.isalnum()):
            raise ValueError()
    except ValueError:
        print("error: username has wrong format, connection refused.")
        exit()
    
    message = "username " + args.Username

    try:
        #define socket using ip4 and TCP
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.settimeout(5)
        clientSocket.connect((serverIP, serverPort))
        #send the encoded upload string to server
        clientSocket.send(message.encode())
        #receive message from Server
        serverMsg = clientSocket.recv(1024).decode()
    except ConnectionRefusedError:
        print("error: server port invalid, connection refused.")
        exit()
    #print(serverMsg)
    
    #username invalid, exit
    if serverMsg == "the username is invalid, already exists":
        print("username illegal, connection refused.")
        exit()

    timelineList = []
    print("username legal, connection established.")
    #prompt command line
    while True:
        print("Command: ", end="")
        commandinput = input()
        #pass in username
        command = commandinput + " " + args.Username
        clientSocket.send(command.encode())
        msg = clientSocket.recv(1024).decode()
        
        #when the message is send to us, append the message to timeline and print the message

        
        if msg.split("\"")[0] == args.Username:
            timelineList.append(msg.split("\"")[3] + ": \"" + msg.split("\"")[1] + "\" " + msg.split("\"")[2])
            print(msg.split("\"")[1])
        elif command.find("timeline") == 0:
            for msg in timelineList:
                print(msg)
        elif msg != "\"not subscribed":
            print(msg)
                
        #print(msg)

        if commandinput == "getusers": 
            res = msg.strip('][').split(', ') 
            for i in range(len(res)):
                #print("user number ", i, ": ", res[i], "\n")
                print(res[i])
            res = None
            msg = None
        
        if commandinput == "gettweets": 
            user = msg
            #for 

        if msg == "bye bye":
            break
    
    #close client socket
    clientSocket.close()
    # except ConnectionRefusedError:
    #     print("Error Message: Server Not Found")
    #     exit()
    # except timeout:
    #     print("Error Message: Session timeout")
    #     exit()
    # except ValueError:
    #     print("Error Message: argument value is invalid")
    #     exit()
    # except OSError:
    #     print("Error Message: Check the ServerIP, no route to host")

if __name__=="__main__":
	main()