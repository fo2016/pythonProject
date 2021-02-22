#import socket module
from socket import *
import sys # In order to terminate the program

def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)

    #Prepare a sever socket
    serverSocket.bind(("", port))
    #Fill in start
    serverSocket.listen(1)
    #Fill in end

    while True:
        #Establish the connection
        print('Ready to serve...')
        connectionSocket, addr =  serverSocket.accept()   #Fill in start      #Fill in end
        try:
            message =  connectionSocket.recv(2048).decode()     #Fill in start    #Fill in end
            filename = message.split()[1]
            f = open(filename[1:])
            outputdata =  f.read() #Fill in start     #Fill in end

            #Send one HTTP header line into socket
            #Fill in start
            #response = "HTTP/1.1 200 OK\r\nContent-Length:" + str(len(outputdata)) + "\r\n\r\n"
            connectionSocket.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n".encode())
            # print('message: ', message)
            # print('filename: ', filename)
            # print('file size:', len(outputdata))
            # print('file content:', outputdata)
            #Fill in end

            #Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())

            connectionSocket.send("\r\n".encode())
            connectionSocket.close()
        except IOError:
            #Send response message for file not found (404)
            #Fill in start
            # print("file not found")
            # print('message: ', message)
            # print('filename: ', filename)
            connectionSocket.send("HTTP/1.1 404 NotFound\r\n\r\n".encode())
            #Fill in end

            #Close client socket
            #Fill in start
            connectionSocket.close()
            #Fill in end

    serverSocket.close()
    sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
    webServer(13331)