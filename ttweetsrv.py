'''
author: Wanli Qian, Junyang Zhang, 
gtid: 903442597
Description: This program features the Server side of the simple tweet application
References: TCPClient.py and TCPServer.py from textbook slides
'''

from socket import *
import argparse
import _thread


usernameList = []
hashtagList = []
hashtagUserDict = {}
tweetTimeLine = {}

def check_hashtag_format(hashtag):
    tags = hashtag.split("#")
    for tag in tags[1:]:
        if not tag.isalnum():
            return True
        if tag == "ALL":
            return True
    return False

def on_new_client(connectionSocket, address):
    while True:
        fromClient = connectionSocket.recv(1024).decode()
        #print("fromClient is: ", fromClient)
        #check tweet
        if fromClient.find("tweet") == 0:
            message = fromClient.split("\"")[1]
            hash_client = fromClient.split("\"")[2]
            hashtag = hash_client.split()[0]
            client = hash_client.split()[1]
            if len(message) > 150:
                failureMsg = "message length illegal, connection refused."
                connectionSocket.send(failureMsg.encode())
            elif len(message) == 0 or message == None:
                failureMsg = "message format illegal."
                connectionSocket.send(failureMsg.encode())
            elif check_hashtag_format(hashtag):
                failureMsg = "hashtag illegal format, connection refused."
                connectionSocket.send(failureMsg.encode())
            else: 
                if tweetTimeLine.get(client) == None: 
                    tweetTimeLine[client] = []
                    tweetTimeLine[client].append(client + ": \"" + message + "\" " + hashtag)
                else:
                    tweetTimeLine[client].append(client + ": \"" + message + "\" " + hashtag)
                split_hashtag = hashtag.split("#")
                for tag in split_hashtag[1:]:
                    tag = "#" + tag
                    for key, value in hashtagUserDict.items():
                        if tag in value:
                            message = key + "\"" + message + "\"" + hashtag + "\"" + client
                            connectionSocket.send(message.encode())
                        elif "#ALL" in value:
                            message = key + "\"" + message + "\"" + hashtag + "\"" + client
                            connectionSocket.send(message.encode())
                connectionSocket.send("\"not subscribed".encode())

        #check subscribe
        elif fromClient.find("subscribe") == 0:
            hashtag = fromClient.split()[1]
            username = fromClient.split()[2]
            if not hashtag.split("#")[1].isalnum():
                failureMsg = "hashtag illegal format, connection refused."
                connectionSocket.send(failureMsg.encode())
            else:
                #new list
                if hashtagUserDict.get(username) == None:
                    userList = []
                    userList.append(hashtag)
                    hashtagUserDict[username] = userList
                    if hashtagList.count(hashtag) == 0 and hashtag != "#ALL":
                        hashtagList.append(hashtag)
                    connectionSocket.send("operation success".encode())
                #append to hashtag list
                else:
                    hashtagUserList = hashtagUserDict.get(username)
                    if hashtagUserList.count(hashtag) == 0:
                        if len(hashtagUserList) != 3:
                            hashtagUserList.append(hashtag)
                            if hashtagList.count(hashtag) == 0 and hashtag != "#ALL":
                                hashtagList.append(hashtag)
                            connectionSocket.send("operation success".encode())
                        else:
                            failureMsg = "sub %s failed, already exists or exceeds 3 limitation" % hashtag
                            connectionSocket.send(failureMsg.encode())  
                    else:
                        failureMsg = "sub %s failed, already exists or exceeds 3 limitation" % hashtag
                        connectionSocket.send(failureMsg.encode())  

        #check unsubscribe                
        elif fromClient.find("unsubscribe") == 0:
            hashtag = fromClient.split()[1]
            username = fromClient.split()[2]
            if not hashtag.split("#")[1].isalnum():
                failureMsg = "hashtag illegal format, connection refused."
                connectionSocket.send(failureMsg.encode())
            else:
                if hashtag == "#ALL":
                    if hashtagUserDict.get(username) != None:
                        hashtagUserDict[username] = []
                else:
                    if hashtagUserDict.get(username) != None:
                        hashtagUserList = hashtagUserDict.get(username)
                        if hashtag in hashtagUserList:
                            hashtagUserList.remove(hashtag)
                connectionSocket.send("operation success".encode())
        #check username
        elif fromClient.find("username") == 0:
            #check if the username already been taken
            username = fromClient.split()[1]
            print('The username from client is : ', username)
            if username in usernameList:
                failureMsg = "the username is invalid, already exists"
                print('current list is', usernameList)
                connectionSocket.send(failureMsg.encode())
                break
            else:
                successMsg = "the username works, already added"
                usernameList.append(username)
                print('current list is', usernameList)
                connectionSocket.send(successMsg.encode())
                
        #check timeline
        elif fromClient.find("timeline") == 0:
            connectionSocket.send("Timeline requested".encode())

        #check getusers
        elif fromClient.find("getusers") == 0:
            connectionSocket.send(("getusers, " + str(usernameList)).encode())

        #check getusers
        elif fromClient.find("getusers") == 0:
            connectionSocket.send(str(usernameList).encode())

        #check gettweet
        elif fromClient.find("gettweets") == 0:
            username = fromClient.split()[1]
            connectionSocket.send(("gettweets, " + str(tweetTimeLine[username])).encode())
        #check exit
        elif fromClient.find("exit") == 0:
            clientName = fromClient.split()[1]
            if clientName in hashtagUserDict:
                del hashtagUserDict[clientName]
            if clientName in tweetTimeLine:
                del tweetTimeLine[clientName]
            usernameList.remove(clientName)
            print("closing ", clientName)
            connectionSocket.send("bye bye".encode())

            break



        #wrong command
        else:
            connectionSocket.send("Wrong command".encode())
        print('global subscribe list is', hashtagList)
        print('global subscribe dict is', hashtagUserDict)
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
        serverSocket.bind(("127.0.0.1", serverPort))
        serverSocket.listen(1)
        print("ServerPort Starts at %s"%serverPort)
        buffer = ""
        while True:
            #Connect with Client and receive message from client
            connectionSocket, address = serverSocket.accept()
            _thread.start_new_thread(on_new_client, (connectionSocket, address))
        serverSocket.close()
            
    except ValueError:
        print("Error Message: serverPort value is invalid")
        exit()


if __name__=="__main__":
	main()