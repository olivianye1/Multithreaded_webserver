"""
COURSE: CMPS 4750 - COMPUTER NETWORKS
ASSIGNMENT: LAB 1 - WEB SERVER LAB
NAME: OLIVIA NYE
SUBMISSION DATE: 03/02/2020
DESCRIPTION: USES PYTHON SOCKET TO CREATE A MULTITHREADED WEBSERVER, CAPABLE OF SERVING MULTIPLE (UP TO 5) SIMULTANEOUS HTTP REQUESTS.
 RENDERS THE CONTENTS OF HelloWorld.html IN THE BROWSER WHEN "/HelloWorld.html" IS APPENDED TO THE PROPER URL. REQUESTS FOR ANY
 PAGES OTHER THAN HELLOWORLD WILL RETURN A 404 ERROR MESSAGE.
"""

from socket import *
import sys  # In order to terminate the program
import os
from _thread import *


def new_thread(cs):
    while True:
        try:
            print("no error")
            message = cs.recv(1024).decode()
            print('message :', message)
            filename = message.split()[1]
            #filename = filename.split('?')[0]
            print('Client request ', filename)
            # get current working directory
            cwd = os.getcwd()
            print('cwd: ', cwd)
            # get full path to file in working directoty
            filePath = cwd + filename
            print('filepath: ', filePath)
            f = open(filePath)
            response = f.read()
            print('response:', response)

            # Send one HTTP header line into socket
            header = 'HTTP/1.1 200 OK\n\n'
            # join header and response into one output var
            outputdata = header + response
            f.close()
            # Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                cs.send(outputdata[i].encode())
            cs.send("\r\n".encode())
            # Close the client connection socket
            cs.close()

        except IOError:
            print("error has occurred:")
            # Send response message for file not found
            header = 'HTTP/1.1 404 Not Found\n\n'
            response = '''
            <html>
                <div>
                    <center>
                        <h1 style="font-weight:bold">
                            Error 404: Not Found
                        </h1>
                    </center>
                </div>
            </html>
            '''
            # join header and response into one output var
            outputdata = header + response
            # Send the error content to the client
            for i in range(0, len(outputdata)):
                cs.send(outputdata[i].encode())
            cs.send("\r\n".encode())
            # Close the client connection socket
            cs.close()


serverSocket = socket(AF_INET, SOCK_STREAM)
# Prepare a sever socket
hostname = gethostname()
hostIp = gethostbyname(hostname)
port = 8000
serverAddress = ('', port)

helloUrl = "http://" + str(hostIp) + ":" + str(port) + "/HelloWorld.html"
errorUrl = "http://" + str(hostIp) + ":" + str(port) + "/HelloWord.html"
print('ACCESS THE SERVER AT THIS ADDRESS to view Hello World: ' + helloUrl + '\n')
print('ACCESS THE SERVER AT THIS ADDRESS to view error: ' + errorUrl + '\n')

# bind the socket to the host and port
serverSocket.bind(serverAddress)

# listen for incoming connections (server mode) with one connection at a time
serverSocket.listen(5)
print("listening.....")

while True:
    # Establish the connection
    print('Ready to serve...')
    # accept external connections
    connectionSocket, addr = serverSocket.accept()
    print(addr)

    start_new_thread(new_thread, (connectionSocket,))
serverSocket.close()

sys.exit()
