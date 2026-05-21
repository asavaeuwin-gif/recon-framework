import socket
import requests
import threading

from colorama import Fore, init
from datetime import datetime

# Initialize colorama
init()

# ==============================
# SAVE RESULTS FUNCTION
# ==============================

def save_result(data):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("results.txt", "a") as file:
        file.write(f"[{timestamp}] {data}\n")


# ==============================
# THREADED PORT SCANNER
# ==============================

def scan_port(target, port):

    try:

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)

        result = s.connect_ex((target, port))

        if result == 0:

            result_text = f"[OPEN] Port {port}"

            print(Fore.GREEN + result_text)

            save_result(result_text)

        s.close()

    except:
        pass


def port_scanner():

    target = input("Enter target: ")

    print(Fore.YELLOW + f"\nScanning {target}...\n")

    save_result(f"Started threaded port scan on {target}")

    threads = []

    for port in range(1, 101):

        thread = threading.Thread(target=scan_port, args=(target, port))

        threads.append(thread)

        thread.start()

    for thread in threads:
        thread.join()

    print(Fore.CYAN + "\nPort scan complete.\n")


# ==============================
# DIRECTORY SCANNER
# ==============================

def directory_scanner():

    target = input("Enter target URL: ")

    wordlist = ["admin", "login", "dashboard"]

    print(Fore.YELLOW + f"\nScanning directories on {target}...\n")

    save_result(f"Started directory scan on {target}")

    for word in wordlist:

        url = f"{target}/{word}"

        try:

            response = requests.get(url)

            result_text = f"[{response.status_code}] {url}"

            print(Fore.CYAN + result_text)

            save_result(result_text)

        except:

            error_text = f"[ERROR] {url}"

            print(Fore.RED + error_text)

            save_result(error_text)


# ==============================
# BANNER GRABBER
# ==============================

def banner_grabber():

    target = input("Enter target: ")
    port = int(input("Enter port: "))

    save_result(f"Started banner grab on {target}:{port}")

    try:

        s = socket.socket()
        s.settimeout(3)

        s.connect((target, port))

        s.send(b"HEAD / HTTP/1.0\r\n\r\n")

        banner = s.recv(1024)

        banner_text = banner.decode(errors="ignore")

        print(Fore.GREEN + "\n[+] Banner Found:\n")
        print(Fore.CYAN + banner_text)

        save_result(banner_text)

        s.close()

    except:

        error_text = "[-] Failed to grab banner."

        print(Fore.RED + error_text)

        save_result(error_text)


# ==============================
# MAIN MENU
# ==============================

while True:

    print(Fore.MAGENTA + """
======== RECON FRAMEWORK ========

1. Threaded Port Scanner
2. Directory Scanner
3. Banner Grabber
4. Exit

=================================
""")

    choice = input("Select option: ")

    if choice == "1":
        port_scanner()

    elif choice == "2":
        directory_scanner()

    elif choice == "3":
        banner_grabber()

    elif choice == "4":
        print(Fore.RED + "Exiting...")
        break

    else:
        print(Fore.RED + "Invalid option.")
