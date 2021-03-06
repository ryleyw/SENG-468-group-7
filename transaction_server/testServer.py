import os
import socket
import string
import sys

HOST = "127.0.0.1"
PORT = 4444

print('Hosting on ' + HOST)

print ('Creating Socket...')
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Prepare a server socket
print('Binding Socket to port ' + str(PORT))	
serverSocket.bind((HOST,PORT)) #Binding sockets to address

serverSocket.listen()
print('Ready to serve...')

while True:
    #Establish the connection
    connectionSocket, addr = serverSocket.accept()
    try:
        command = connectionSocket.recv(1024)
        command = command.decode()
        command = eval(command)
        #print(command)
        if command[0] == 'ADD':
            print('Adding funds to user account')
            addInfo = command[2] + " was deposited into " + command[1] + "'s account."
            connectionSocket.send(addInfo.encode())
        elif command[0] == 'BUY':
            print('Buying Stonks')
            connectionSocket.send("Stonks added".encode())
        elif command[0] == 'QUOTE':
            print('Checking quote...')
            quoteRequest = command[2] + "," + command[1] + "\n"
            #print(quoteRequest.encode())
            quoteServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            quoteServer.connect(('quoteserver.seng.uvic.ca',4444))
            quoteServer.send(quoteRequest)
            quote = quoteServer.recv(1024)
            #print(quote.decode())
            quoteServer.close()
            quoteInfo = quote.decode().split(",")
            #print(quoteInfo)
            quotePrice = "Price of " + quoteInfo[1] + " is " + quoteInfo[0]
            connectionSocket.send(quotePrice.encode())
        else:
            connectionSocket.send("Command could not be found".encode())
        connectionSocket.close()
    except IOError:
        print("Error")
        connectionSocket.close()
serverSocket.close()
sys.exit()