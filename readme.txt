Name: Wanli Qian, Junyang Zhang, Yuqi He

PA2/
README.txt  -description of the project and semantics of implementation
ttweetcl.py -client side of simple tweet application
ttweetsrv.py -server side of simple tweet application

Yuqi He was responsible for subscribe unsubscribe
JunyangZhang was responsible for Tweet and Timeline
Wanli Qian was responsible for getusers, gettweets, duplicate user check, exit

Run Server, specify the serverport. 
usecase: python3 ttweetsrv.py 13500

Then run client and specify serverIP serverport and username 
usecase: python3 ttweetcl.py 127.0.0.1 13500 wq
Once the client is started, it will continue to listen to user input command 

The uses cases for input command are as follows:
tweet “<150 char max tweet>” <Hashtag> 
This allows user to tweet to a Hashtag

subscribe <Hashtag>
Allows user to subscribe to a hashtag

unsubscribe <Hashtag>
Allows user to unsubscribe to a hashtag

timeline
Prints all tweets that have been sent to it by the server

getusers
Prints all users currently online

gettweets <Username>
Print all historical tweets sent by the specified user

exit
Disconnect from the server and clean up all the leftover states.

before running our code: make sure you have argparse package by "pip install argparse"

