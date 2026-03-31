
from colorama import init, Fore, Style, Back


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

def generate_ascii():
 print(f"""
{COLOR_MAGENTA}
  ██████████ ██████  ███████      ███████        ███████     ███████         ███████             ███   ████████████
      ██     ██      ██     █     ██     █     ██       ██   ██     █        ██     █           █████       ██
      ██     ██      ██      █    ██      █   ██         ██  ██      █       ██      █         ██   ██      ██
      ██     █████   ████████     ████████    ██         ██  ████████        ████████         █████████     ██
      ██     ██      ██     ██    ██     ██   ██         ██  ██     ██       ██      ██      ██       ██    ██
      ██     ██      ██      ██   ██      ██   ██       ██   ██      ██      ██       ██    ██         ██   ██
      ██     ██████  ██       ██  ██       ██    ███████     ██       ██     ██        ██  ██           ██  ██
   ╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════╝
{COLOR_RESET}
""")
# --- Constants for Messages ---
INFO = f"{COLOR_INFO}[INFO] {COLOR_RESET}"
DOWNLOAD = f"{COLOR_SECONDARY}[DOWNLOAD] {COLOR_RESET}"
UPLOAD = f"{COLOR_SECONDARY}[UPLOAD] {COLOR_RESET}"
ERROR = f"{COLOR_ERROR}[ERROR] {COLOR_RESET}"
COMMAND_PROMPT = f"{COLOR_PRIMARY}TerrorRAT {COLOR_ACCENT}>> {COLOR_RESET}"
CONNECTION_LOST = f"{COLOR_ERROR}Connection lost with client.{COLOR_RESET}"



def display_menu():
        generate_ascii()
        print("\n" + COLOR_SECONDARY + "="*120)
        print(COLOR_SECONDARY + "="*120)
        print(f"{COLOR_ACCENT}            Operations Menu")
        print(f"{COLOR_SECONDARY}----------------------------------------------------------")
        print(f"{COLOR_PRIMARY}  File Operations:")
        print(f"    download {COLOR_WARNING}<client_path>{COLOR_PRIMARY}   - Download file from client")
        print(f"    upload {COLOR_WARNING}<local_path>{COLOR_PRIMARY}      - Upload file to client")
        print(f"{COLOR_PRIMARY}  System Operations:")
        print(f"    screenshot             - Take a screenshot of the client")
        print(f"    cd {COLOR_WARNING}<directory>{COLOR_PRIMARY}           - Change directory on client")
        print(f"{COLOR_PRIMARY}  Execution:")
        print(f"{COLOR_WARNING}   <command>{COLOR_PRIMARY}                 - Execute a shell command")
        print(f"{COLOR_PRIMARY}  Other:")
        print(f"    help                   - Show this menu")
        print(f"    about                   - It's obvious :)")
        print(f"    Exit                   - Disconnect client and exit server")
        print(f"{COLOR_WARNING}\n\nNote:{COLOR_PRIMARY} If you want to take advantage of 'sudo', you should specify -S to take the password from stdin\n(Example: echo 'password' | sudo -S apt-get update)")
        print(COLOR_SECONDARY + "="*60 + COLOR_RESET + "\n")

def about():
    
    print("\n" + COLOR_SECONDARY + "="*120)
    print(f"{COLOR_ACCENT}       About Us")
    print(f"{COLOR_SECONDARY}----------------------------------------------------------")
    print(f"{COLOR_PRIMARY}In endless twilight the shadow army")
    print(f"{COLOR_PRIMARY}is birthed ")
    print(f"{COLOR_PRIMARY}they breed disease")
    print(f"{COLOR_PRIMARY}they rot the core ")
    print(f"{COLOR_PRIMARY}and silence the screams")
    print(f"{COLOR_SECONDARY}The king of plague rats sits in judgement.\n")

