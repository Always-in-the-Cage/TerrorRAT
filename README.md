# 🐀 TerrorRAT

> *"In endless twilight the shadow army is birthed..."*

TerrorRAT is a custom-built, Python-based Remote Access Tool (RAT) / Command and Control (C2) server. It utilizes SSL/TLS encryption for secure communication between the server and the client, allowing for remote system administration, file transfers, and execution.

⚠️ **Disclaimer:** This tool was developed for educational purposes, authorized penetration testing, and personal use ONLY. The developer assumes no liability and is not responsible for any misuse or damage caused by this program.

## ⚡ Features
*   **Encrypted Traffic:** Uses SSL/TLS sockets (`ssl.wrap_socket`) to keep communications secure.
*   **Remote Shell Execution:** Execute shell/Powershell commands remotely.
*   **File Operations:** Seamlessly upload and download files between the C2 and the client.
*   **Stealth Screenshots:** Capture the client's screen remotely and save it locally.
*   **Directory Navigation:** Change directories (`cd`) smoothly on the target machine.
*   **Cross-Platform:** Client runs on both Windows (uses PowerShell) and Linux.

## 🛠️ Prerequisites

*   Python 3.x
*   `colorama` (for the C2 server interface)
*   `pyautogui` (for client screenshot capabilities)
*   `openssl` (for generating certificates)

Install Python dependencies:
```bash
pip install -r requirements.txt

## 🚀 Usage

### 1. Generate SSL Certificates
Before starting the server, you need to generate your self-signed SSL certificates. A setup script is provided.
bash
chmod +x setup.sh
./setup.sh
*This will generate `server.key` and `server.crt` in your directory.*

### 2. Start the C2 Server
Run the server script and follow the prompts to bind your IP and Port.
bash
python server.py

### 3. Start the Client
Run the client script on the target machine. It will prompt for the C2 server's IP and Port.
bash
python client.py
*(Alternatively, you can compile the client into a standalone executable using the provided `client.spec` file with PyInstaller: `pyinstaller client.spec`)*

## 🪧 C2 Menu Commands
*   `download <client_path>` - Download a file from the client.
*   `upload <local_path>` - Upload a file to the client.
*   `screenshot` - Take a screenshot of the client's current screen.
*   `cd <directory>` - Change working directory.
*   `help` - Show the interactive menu.
*   `Exit` - Kill the connection.

---
*The king of plague rats sits in judgement.*
