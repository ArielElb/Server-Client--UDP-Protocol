from socket import *
import sys


def runClient():
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    while clientSocket:
        msg = input()

        if msg:
            serverIP = sys.argv[1]
            serverPort = int(sys.argv[2])

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
