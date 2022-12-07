from socket import *
import sys

"""
function to check if client is already joined.
"""
def checkIfClientIsInList(clientAddress, clientMsg):
    for client in clientMsg.values():
        if client['client'] == clientAddress:
            return True
    return False


"""
adding a Client to the dictionary  , and letting the other clients that a new client joined.
"""
def addClientToDict(clientAddress, clientDict, name, serverSocket, clientHasJoined):
    # if someone has already joined the chat
    if clientDict.keys():
        # if the client already joined the chat
        # send the message to all the clients in the list.
        for client in clientDict.values():
            if client['client'] == clientAddress:
                continue
            # Send to all the clients in the list that the user has joined.
            else:
                client['msgs'].append(clientHasJoined)

        # send the names to the client
        listNames = list(clientDict)
        listNames.reverse()
        namesList = ', '.join(str(e) for e in listNames)
        serverSocket.sendto(bytes(namesList, 'utf-8'), clientAddress)
        clientDict[name] = {'client': clientAddress, 'msgs': []}
    else:
        # this is the first client to join the chat.
        clientDict[name] = {'client': clientAddress, 'msgs': []}
        serverSocket.sendto(bytes('', 'utf-8'), clientAddress)


"""
a client send a massage to all the clients.
"""
def sendMsgToAllClients(clientDict, clientAddress, msg, serverSocket):
    clientName = ''
    for nameOfClient, clientMsgDict in clientDict.items():
        if clientMsgDict['client'] == clientAddress:
            clientName = nameOfClient
    nameMsg = clientName + ': ' + str(msg.decode()[2::])
    for client in clientDict.values():
        if client['client'] == clientAddress:
            continue
        # Send to all the clients in the list that the user has joined.
        else:
            client['msgs'].append(nameMsg)
    serverSocket.sendto(bytes('', 'utf-8'), clientAddress)


"""
let client change his name and let the other clients that the client has changed his name.
"""
def changeClientName(clientDict, clientAddress, name, serverSocket):
    newClientName = name
    oldN = ''
    for oldName, clientMsgDict in clientDict.items():
        if clientMsgDict['client'] == clientAddress:
            oldN = oldName
            clientDict[newClientName] = clientDict[oldName]
            del clientDict[oldName]
            serverSocket.sendto(bytes('', 'utf-8'), clientAddress)
            break

    for client in clientDict.values():
        if client['client'] == clientAddress:
            continue
        # Send to all the clients in the list that the user has joined.
        else:
            client['msgs'].append(f"{oldN} changed his name to {newClientName}")

"""
client has left the chat, update the dictionary accordingly and update it for the other clients.
"""
def clientLeave(clientDict, clientAddress, serverSocket):
    clientName = ''
    for clName, clientMsgDict in clientDict.items():
        if clientMsgDict['client'] == clientAddress:
            clientName = clName

    for client in clientDict.values():
        client['msgs'].append(f"{clientName} has left the chat")
    del clientDict[clientName]
    serverSocket.sendto(bytes('', 'utf-8'), clientAddress)

"""
show all the massages that are waiting for the client ,to the client who chose option 5.
"""
def showUpdates(clientDict, clientAddress, serverSocket):
    for client in clientDict.values():
        if client['client'] == clientAddress:
            # if the client don't have msgs
            if not client['msgs']:
                serverSocket.sendto(bytes('', 'utf-8'), clientAddress)
                continue
            clientMsgs = '\n'.join(str(e) for e in client['msgs'])
            serverSocket.sendto(bytes(clientMsgs, 'utf-8'), clientAddress)
            client['msgs'] = []

"""
send an error msg if the restrictions arnt valid.
"""
def sendError(serverSocket, clientAddress):
    serverSocket.sendto(bytes('Illegal request', 'utf-8'), clientAddress)


def runServer():
    # second argument is the server Port
    if len(sys.argv) < 2:
        return
    serverPort = sys.argv[1]
    # if the serverPort is not a number
    if not serverPort.isnumeric():
        return
    # the port is a number.
    serverPort = int(sys.argv[1])
    if serverPort < 0 or serverPort > 65535:
        return
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    clientDict = {}
    while True:

        # receive message from client and save the client address - (IP, port).
        msg, clientAddress = serverSocket.recvfrom(1024)
        # the name of the user for the JOIN function.
        name = str(msg.decode()[2::])
        # flag to check if client already joined.
        clientHasJoined = f"{name} has joined"
        # the option the user wanted to do
        OPTION = msg.decode()[0]
        JOIN = '1'
        SEND_MSG = '2'
        CHANGE_NAME = '3'
        LEAVE = '4'
        SHOW_UPDATES = '5'
        # check if the user has joined already.
        isJoined = checkIfClientIsInList(clientAddress, clientDict)
        if OPTION == JOIN and isJoined:
            print('Illegal request')
            continue

        elif (not isJoined) and OPTION != JOIN:
            serverSocket.sendto(bytes('Illegal request', 'utf-8'), clientAddress)
            continue

        # if user want to join and all restrictions are valid.
        elif OPTION == JOIN and len(str(msg.decode())) >= 3 and str(msg.decode())[1] == ' ':
            addClientToDict(clientAddress, clientDict, name, serverSocket, clientHasJoined)
        # if user want to send a message and all restrictions are valid.
        elif OPTION == SEND_MSG and isJoined and len(msg.decode()) >= 3 and str(msg.decode())[1] == ' ':
            sendMsgToAllClients(clientDict, clientAddress, msg, serverSocket)
        # if user want to change his name and all restrictions are valid.
        elif OPTION == CHANGE_NAME and len(msg.decode()) >= 3 and str(msg.decode())[1] == ' ':
            changeClientName(clientDict, clientAddress, name, serverSocket)
        # if user want to leave the chat and all restrictions are valid.
        elif OPTION == LEAVE and isJoined and len(str(msg.decode())) == 1:
            clientLeave(clientDict, clientAddress, serverSocket)
        # if user want to see all the updates and all restrictions are valid.
        elif OPTION == SHOW_UPDATES and isJoined and len(str(msg.decode())) == 1:
            showUpdates(clientDict, clientAddress, serverSocket)
            # if the is an error send error to the client.
        else:
            sendError(serverSocket, clientAddress)


if __name__ == '__main__':
    runServer()
