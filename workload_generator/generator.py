import socket
import sys
import time
import re

HOST = "127.0.0.1"
PORT = 4444
filename = "1userWorkLoad.txt"
request_list = []

f = open(filename, "r")
lines = f.read().split(' \n')

#Split each line into a list of lists
for command in lines:
    command = re.sub("\[[0-9]+]\s", "", command) #Removes indexing from each line ie. [1-100]
    command_list = command.split(',')
    request_list.append(command_list)

#print(request_list)

print('Connecting to ' + HOST + ' with port ' + str(PORT))

#Sends each user request to transaction server
for request in request_list:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((HOST, PORT))
    clientSocket.send(str(request).encode())
    response = clientSocket.recv(1024).decode()
    print(response)