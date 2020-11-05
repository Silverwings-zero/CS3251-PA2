Name: Junyang Zhang

E-mail: jzhang3027@gatech.edu

Files submitted:
    ttweetcl.py
    - This file is the client. 
    - The port number has to be >= 13000 and <=14000 incorrect format will result in "Error: Incorrect port number format"
    - If the client can not connect to server, it will show "Error Message: Server Not Found"
    - If message has 0 characters or longer than 150 characters, it will show "Message is longer than 150 characters or has 0 characters"
    ttweetsrv.py
    - This file is the server file. 
    - The port number has to be >= 13000 and <=14000 incorrect format will result in "Error: Incorrect port number format"

Instructions:
    - First start the server by running: python ttweetsrv.py <ServerPort>
    - Then run the client using the following command when trying to upload a message: python ttweetcl.py -u <ServerIP> <ServerPort> "message"
    - Run the client using the following command when trying to download a message: python ttweetsrv.py -d <ServerIP> <ServerPort>

Output sample will be provided in the Sample.txt file

Protocol description:
    Once the server is run, it will constantly look for connection. This is implemented using an infinite while loop. If a connection is established with the client, the sever proceeds to store the message or send the encoded stored message back to the client based on the client's query. The client decodes the message and prints the message.
    The TCP socket is used for server. It listens to a particular port of the server based on the user entry.
    The client can access the server. If the user entered in correct amount of inputs, an error will be printed. If the format of inputs are correct and the mode is upload, the message is encoded and sent to server. If the format of inputs are correct and the mode is download, the last uploaded message will be decoded and received from server. 
    