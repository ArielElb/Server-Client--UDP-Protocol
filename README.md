<h4 align="center">


![](https://github.com/TopazAvraham/IntroductionToCS-University-C-programming/blob/master/Screenshots/31.png?raw=true)

</h4>

<h4 align="center">Implementation of client & server code which acts similar to WhatsApp groups!</h4>

<p align="center">
  <a href="##Introduction">Introduction</a> •
  <a href="#Screenshots">Implementation</a> •
   <a href="#Screenshots">Example</a> •
  <a href="#Installation">Installation</a> •
  <a href="#Author">Author</a> •
</p>



## Introduction

This Server & Client code is the final product of computer-networks course assignment, which I took in the 1st semester of my 2nd year at Bar Ilan University.  
I implemeted code which acts like WhatsApp-groups, in where each user (client) can:


💥 Join the group

💥 Send messages to all other members of the group.

💥 Change his name for future messages

💥 Get notifications about other people's activity in the group- when someone else has joined, sent a message, left the group, etc.


## Implementation

Our chat will act similar to a Whatsapp group, in which each member can write a message, and every message someone writes is sent to all other memebers. <br>
When someone is sending a message, the message is being sent to the server immediately. Yet, the server sents the message to the other memebers only when they reach out the server. <br>

For example: Alice, Bob, and Charlie are members in the group. Alice sent a message. The message needs to be sent to Bob and Charlie, <br>
but they will receive Alice's message only when they ask for it explicitly from the server, or if they will send a message to the server so he will send them back all their waiting messages. <br>

Our server is establishing a socket and listens on the port number which he receives as an argument from CLI.<br><br>
<b>The server can receive 5 different types of messages:</b><br> <br>

1. <b>Register- Client which sends this message, wants to join the group chat.</b> <br>
    The message will be in the following format: 1 [Name]<br>
    
    The server keeps details of the client's name and socket details, and sends all other members the message: [Name] has joined.<br>
    Also, the server sends to the client who asked to join all names of the existing members in the group. <br><br><br>
       
2. <b>Sending a message-  Client wants to send a message to all other members in the group.</b><br>
    The message will be in the following format: 1 [Name]: [Message]<br><br><rb>
  
3. <b>Change of name- Client which sends this message, wants to change his name in the group.</b><br>
    The message will be in the following format: 3 [Name]<br>
    
    When the server recieves this type of message, it sends all other members the message: <br>[Old Name] changed his name to [New Name].<br><br>
  
4. <b>leaving the group- Client which sends this message, wants to leave the group.</b><br>
    The message will be in the following format: 4<br>
    
    When the server recieves this type of message, it sends all other members the message: [Name] has left the group.<br><br>
  
 5. <b>Get new info- Client which sends this message, wants to get notification abut all new messages since his last update. </b><br>
    The message will be in the following format: 5<br>
    
    When the server recieves this type of message, it sends the client 1 message that contain all the messages <br> 
  that were supposed to be sent to him since the last time. <br><br>
    

## Example
  <b>
    1. Alice registered. <br>
    2. Bob registered. <br>
    3. Bob sent a message.<br>
    4. Display so far:<br>
    <p align="left">
  <img width="1000" height="325" src="https://github.com/TopazAvraham/IntroductionToCS-University-C-programming/blob/master/Screenshots/תמונה1.png?raw=true">
</p>
    5. Charlie registered.<br>
    6. Charlie sent 2 messages.<br>
    7. Display so far:<br>
    <p align="left">
  <img width="1000" height="325" src="https://github.com/TopazAvraham/IntroductionToCS-University-C-programming/blob/master/Screenshots/תמונה2.png?raw=true">
</p>    
    8. Alice asked for update.<br>
    9. Display so far:<br>
      <img width="1000" height="320" src="https://github.com/TopazAvraham/IntroductionToCS-University-C-programming/blob/master/Screenshots/תמונה3.png?raw=true">
</p>    
    10. Alice sent a message.<br>
    11. Alice sent invalid message.<br>
    12. Charlie changed his name.<br>
    13. Charlie sent a message.<br>
    14. Display so far:<br>
      <img width="1000" height="325" src="https://github.com/TopazAvraham/IntroductionToCS-University-C-programming/blob/master/Screenshots/תמונה4.png?raw=true">
</p>    
    15. Charlie left.<br>
    16. Bob sent a message.<br>
    17. Alice asked for update.<br>
    18. Display so far:<br>
      <img width="1000" height="355" src="https://github.com/TopazAvraham/IntroductionToCS-University-C-programming/blob/master/Screenshots/תמונה5.png?raw=true">
</p>    
  

## Installation - How To Run Code
<b>

1. Clone this repo by creating a specific folder in your computer, open terminal in this folder and run this command:
    ```
    git clone https://github.com/OzAmoyal/GroupChat--Using-UDP-Sockets.git
    ```
    Alternatively, you can just download all the files from this repo to your computer, and save them all in that specific folder

2. Open different “terminals” in this specific folder.<br>
	
3. Run this command in one terminal to run the server code:
	```
    python3 server.py (para1)
    ```
	
	where para1 = port number that the server will listen to.
  <br>
  
5. Run this command in a second terminal to run the client code:
	```
    python3 client.py (para1) (para2)
    ```
	
  where para1 = IP address of the server <br>
	and para2 = Port number of the server <br>
  
6. You can also open as many terminals as you wish to illustrate different clients.
  
7. Start chatting in the group and enjoy the results.

</b>	

## Built With

- Python
- UDP Sockets


