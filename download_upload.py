import socket
import os
import struct

class Download_and_Upload:

    def __init__(self,connected_socket):
        self.connected_socket=connected_socket

    def receive_all(self,total_bytes):
        data=bytearray()
        while len(data)<total_bytes:
            packet = self.connected_socket.recv(total_bytes - len(data))
            if not packet:
                return None
            data.extend(packet)
        return bytes(data)

    def download(self,file_name):

        response = self.connected_socket.recv(len("Yes".encode()))
        if response==b"": # this means that client has disconnected, so it returns an empty string
            return
        if response =="Yes".encode():
            total_response=b""
            print("Downloading file...\n")
            

            header=self.receive_all(4)
            response_length = struct.unpack('>I', header)[0]
            response = self.receive_all(response_length)
            if response==b"": # this means that client has disconnected, so it returns an empty string
                return
            total_response+=response

            with open(file_name,"xb") as file:
                file.write(total_response)
                print("File downloaded successfully.\n")


        else:
            print("File does not exist!Try again...\n")

    def upload(self,path_input):
        if os.path.exists(path_input):
            chunk = "Yes".encode()
            self.connected_socket.send(chunk)
            chunk=b""
            with open(path_input,"rb") as file:
                chunk += file.read()
                chunk_header=struct.pack('>I',len(chunk))
                self.connected_socket.sendall(chunk_header+chunk)
