
import socket
import requests
import threading
import json

from colorama import Fore, init
from datetime import datetime

# Initialize colorama
init()

# ==============================
# GLOBAL RESULTS STORAGE
# ==============================

scan_results = []

# ==============================
# SAVE RESULTS FUNCTION
# ==============================

def save_result(data):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"[{timestamp}] {data}"

    with open("results.txt", "a") as file:
        file.write(log_entry + "\n")

    scan_results.append({
        "timestamp": timestamp,
        "result": data
    })


# ==============================
# EXPORT JSON REPORT
# ==============================

def export_json():

    with open("results.json", "w") as json_file:

        json.dump(scan_results, json_file, indent=4)

    print(Fore.GREEN + "\n[+] JSON report exported successfully.\n")


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
# SECURITY HEADER SCANNER
# ==============================

def security_header_scanner():

    target = input("Enter target URL: ")

    print(Fore.YELLOW + f"\nChecking security headers on {target}...\n")

    save_result(f"Started security header scan on {target}")

    try:

        response = requests.get(target)

        headers = response.headers

        security_headers = [
            "X-Frame-Options",
            "Content-Security-Policy",
            "Strict-Transport-Security",
            "X-Content-Type-Options"
        ]

        for header in security_headers:

            if header in headers:

                result_text = f"[FOUND] {header}: {headers[header]}"

                print(Fore.GREEN + result_text)

                save_result(result_text)

            else:

                result_text = f"[MISSING] {header}"

                print(Fore.RED + result_text)

                save_result(result_text)

    except:

        error_text = "[ERROR] Failed to scan headers."

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
4. Security Header Scanner
5. Export JSON Report
6. Exit

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
        security_header_scanner()

    elif choice == "5":
        export_json()

    elif choice == "6":
        print(Fore.RED + "Exiting...")
        break

    else:
        print(Fore.RED + "Invalid option.")
