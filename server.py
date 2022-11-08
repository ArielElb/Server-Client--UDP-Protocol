from socket import *
import sys


def checkIfClientIsInList(clientAddress, clientMsg):
    for client in clientMsg.values():
        if client['client'] == clientAddress:
            return True
    return False


def runServer():
    # second argument is the server Port
    serverPort = int(sys.argv[1])
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    EMPTY_MSG = 'EMPTY'
    clientDict = {}
    while True:
        # receive message from client and save the client address - (IP, port).
        msg, clientAddress = serverSocket.recvfrom(1024)
        name = str(msg.decode()[2::])
        clientHasJoined = f"{name} has joined"
        typeOfAction = msg.decode()[0]
        isJoined = checkIfClientIsInList(clientAddress, clientDict)
        if typeOfAction == '1' and isJoined:
            print('Illegal request')
            continue

        elif (not isJoined) and typeOfAction != '1':
            serverSocket.sendto(bytes('Illegal request', 'utf-8'), clientAddress)
            continue

        elif typeOfAction == '1' and len(str(msg.decode())) >= 2 and str(msg.decode())[1] == ' ':
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

        elif typeOfAction == '2' and isJoined and len(msg.decode()) >= 3 and str(msg.decode())[1] == ' ':
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

        elif typeOfAction == '3' and len(msg.decode()) >= 3 and str(msg.decode())[1] == ' ':
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

        elif typeOfAction == '4' and isJoined and len(str(msg.decode())) == 1:
            clientName = ''
            for clName, clientMsgDict in clientDict.items():
                if clientMsgDict['client'] == clientAddress:
                    clientName = clName

            for client in clientDict.values():
                client['msgs'].append(f"{clientName} has left the chat")
            del clientDict[clientName]
            serverSocket.sendto(bytes('', 'utf-8'), clientAddress)

        elif typeOfAction == '5' and isJoined and len(str(msg.decode())) == 1:
            for client in clientDict.values():
                if client['client'] == clientAddress:
                    # if the client don't have msgs
                    if not client['msgs']:
                        serverSocket.sendto(bytes('', 'utf-8'), clientAddress)
                        continue
                    clientMsgs = '\n'.join(str(e) for e in client['msgs'])
                    serverSocket.sendto(bytes(clientMsgs, 'utf-8'), clientAddress)
                    client['msgs'] = []
        else:
            serverSocket.sendto(bytes('Illegal request', 'utf-8'), clientAddress)


if __name__ == '__main__':
    runServer()
