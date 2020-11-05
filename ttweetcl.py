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
    argument 1: optional flag -u or -d indicating upload mode or download mode, must include either one
    argument 2: positional argument ServerIP the name of the Server in dotted format
    argument 3: positional argument ServerPort indicate which port the user wants to connect
    argument 4: optional flag -m: message flag only required if the -u is specified in argument 1
    argument 5: optional argument message content
    '''
    parser = argparse.ArgumentParser(description= 'minitweet client side')
    mul = parser.add_mutually_exclusive_group(required = True)
    mul.add_argument('-u',action="store_true")
    mul.add_argument('-d',action="store_true")
    parser.add_argument('ServerIP', type = str)
    parser.add_argument('ServerPort', type = int)

    parser.add_argument('-m', type = str, required = '-u' in sys.argv)
    #attaching function run
    parser.set_defaults(func=run)
    args = parser.parse_args()

    args.func(args)


def run(args):
    #check Server Ip formatting, raise exception if the input ip doesn't follow the standard format
    try:
        IP = inet_aton(args.ServerIP)
        serverIP = str(args.ServerIP)
    except:
        print("Error, invalid server ip")
        exit()

    try:
        serverPort = int(args.ServerPort)
        #check serverPort value, raise error if server port is out of bound
        #if serverPort < 1000 or serverPort > 65535:
        #    raise ValueError

        #Determine whether the client is in upload mode or download mode
        if args.u == True:
            # check message length, raise error if longer than 150
            if len(args.m) > 150:
                raise ValueError
            else:
                #edit the first two characters of upload string to indicate upload mode as well as append the message
                message = '-u' + args.m
        else:
            # edit the first two characters of upload string to indicate download mode
            message = '-d'

        #define socket using ip4 and TCP
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.settimeout(5)
        clientSocket.connect((serverIP, serverPort))
        #send the encoded upload string to server
        clientSocket.send(message.encode())
        #receive message from Server
        serverMsg = clientSocket.recv(1024)
        #Formatting message considering different modes
        if args.d == True:
            print("\""+serverMsg.decode()+"\"")
        else:
            print(serverMsg.decode())
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