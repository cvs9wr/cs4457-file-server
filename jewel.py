#!/usr/bin/env python3

import socket
import sys
import os
from file_reader import FileReader
import select
import queue

class Jewel:

    def __init__(self, port, file_path, file_reader):
        self.file_path = file_path
        self.file_reader = file_reader
        file_data = FileReader()
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(False)
        server.bind(('0.0.0.0', port))

        print('Server started on port '+str(port))

        server.listen(5)

        inputs = [ server ]

        outputs = [ ]

        message_queue = {}
        #This waits for input, which will never run out because the list will always have an open server socket
        while inputs:
            #Break down a given input on the socket into what we are going to read and send back. These are all queues
            readable, writable, exceptional = select.select(inputs, outputs, inputs)
            for s in readable:
                if s is server:
                    #Establish a new connection with the client and append it as a potential place to read data from
                    client, address = s.accept()
                    print("[CONN] Connection from "+str(address)+"on port "+str(port))
                    client.setblocking(1)
                    inputs.append(client)
                    message_queue[client] = queue.Queue()
                #Client is already in our queue of potential messagers, cap all inputs at 1024 and then parse the data for the filepath they requested
                else:
                    data = s.recv(1024)
                    if data:
                        potential_cmd = b''
                        potential_filepath = b''
                        try:
                            potential_cmd = data[0:data.index(b' ')]
                            #print("potentialcmd: "+str(potential_cmd))
                        #requested a file that the server does not have
                        except:
                            print("[ERRO] ["+str(address)+":"+str(port)+"] "+str(data)+" request returned error 500") 
                        #Browser used a method that was not GET HEAD OR QUIT
                        if (b'GET' not in data and b'HEAD' not in data and b'QUIT' not in data):
                            print("501 Method Unimplemented") 
                        #Check that the command was not malformed
                        if (potential_cmd != b''):
                            try:
                                potential_filepath = data[data.index(b' ')+1:-1]
                                potential_filepath = potential_filepath[0:potential_filepath.index(b' ')]
                            except: 
                                print("[ERRO] ["+str(address)+":"+str(port)+"] "+str(data)+" request returned error 500 (likely invalid command syntax)")
                            #Command not malformed, parse as either a GET or HEAD Request
                            if (potential_cmd == b'GET'):
                                print("[REQU] ["+str(address)+":"+str(port)+"] GET request for "+str(potential_filepath))
                                #print(file_data.get(b''+potential_filepath, 'idk'))
                                client_message = file_data.get(b''+file_path.encode()+potential_filepath, 'idk')
                                print("CM: "+str(len(client_message)))
                                message_queue[s].put(client_message)
                                if b'404 Not Found' in client_message:
                                    print(print("[ERRO] ["+str(address)+":"+str(port)+"] "+str(data)+" request returned error 404 Not Found"))
                            if (potential_cmd == b'HEAD'):
                                client_message = file_data.head(b''+file_path.encode()+potential_filepath, 'idk')
                                if client_message == None:
                                    message_queue[s].put((b'HTTP/1.1 404 Not Found\n'
                                                +b'Content-Type: text/html\n'
                                                +b'Content-Length: 50\n'
                                                +b'Servers: cvs9wr\n'
                                                +b'\n'+b'<html><body><h1>file not found</h1></body> </html>'))
                                else:
                                    message_queue[s].put(b'Content-Length: 5\n'+b'Server: cvs9wr\n'+b'Content-Type: text/plain\n\n'+client_message)
                        if s not in outputs:
                            outputs.append(s)
                    else:
                        if s in outputs:
                            outputs.remove(s)
                        inputs.remove(s)
                        s.close()
            #Handle logic for sending messages back to the user
            for s in writable:
                try:
                    next_message = message_queue[s].get_nowait()
                    #print(next_message)
                except queue.Empty:
                    outputs.remove(s)
                else:
                    val = s.send(next_message)
                    print("val: "+str(val))
                    print("nextmsg: "+str(len(next_message)))
                    check = 0
                    check = len(next_message)
                    #while (val <= check):
                    #    val += s.send(next_message[val:-1])  
            for s in exceptional:
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                s.close()
            #print(data[0:-1])
            
        
if __name__ == "__main__":
    port = int(sys.argv[1])
    file_path = sys.argv[2]

    FR = FileReader()

    J = Jewel(port, file_path, FR)
