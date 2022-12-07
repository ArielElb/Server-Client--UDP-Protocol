from socket import *
import sys


def runClient():
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    if len(sys.argv) < 3:
        return
    while clientSocket:
        msg = input()
        if msg:
            if len(msg) == 2:
                print("Illegal request")
                continue
            serverIP = sys.argv[1]
            serverPort = sys.argv[2]
            # if the server port isnt a number.
            if not serverPort.isnumeric():
                clientSocket.close()
                break
           # the port is a number.
            serverPort = int(sys.argv[2])
            if serverPort < 0 or serverPort > 65535:
                clientSocket.close()
                break
            clientSocket.sendto(msg.encode(), (serverIP, serverPort))
            data, serverAddress = clientSocket.recvfrom(2048)
            if str(data.decode()) == '' and msg == '4':
                clientSocket.close()
                break
            elif str(data.decode()) == '':
                continue
            print(str(data.decode()))
        else:
            print('Illegal request')


if __name__ == '__main__':
    runClient()
