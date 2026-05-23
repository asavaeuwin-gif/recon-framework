import socket
import requests
import threading
import json

from colorama import Fore, init
from datetime import datetime

# Initialize colors
init()

scan_results = []


# =========================
# SAVE RESULTS
# =========================

def save_result(data):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("results.txt", "a") as file:
        file.write(f"[{timestamp}] {data}\n")

    scan_results.append({
        "timestamp": timestamp,
        "result": data
    })


# =========================
# EXPORT JSON
# =========================

def export_json():

    with open("results.json", "w") as file:
        json.dump(scan_results, file, indent=4)

    print(Fore.GREEN + "\n[+] JSON report exported.\n")


# =========================
# PORT SCANNER
# =========================

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

    threads = []

    for port in range(1, 101):

        thread = threading.Thread(
            target=scan_port,
            args=(target, port)
        )

        threads.append(thread)

        thread.start()

    for thread in threads:
        thread.join()

    print(Fore.CYAN + "\nScan complete.\n")


# =========================
# DIRECTORY SCANNER
# =========================

def directory_scanner():

    target = input("Enter target URL: ")

    wordlist = [
        "admin",
        "login",
        "dashboard"
    ]

    print(Fore.YELLOW + "\nScanning...\n")

    for word in wordlist:

        url = f"{target}/{word}"

        try:

            response = requests.get(url)

            result = f"[{response.status_code}] {url}"

            print(Fore.CYAN + result)

            save_result(result)

        except:

            print(Fore.RED + f"[ERROR] {url}")


# =========================
# BANNER GRABBER
# =========================

def banner_grabber():

    target = input("Enter target: ")
    port = int(input("Enter port: "))

    try:

        s = socket.socket()

        s.settimeout(3)

        s.connect((target, port))

        s.send(b"HEAD / HTTP/1.0\r\n\r\n")

        banner = s.recv(1024)

        text = banner.decode(
            errors="ignore"
        )

        print(Fore.GREEN + "\nBanner:\n")

        print(Fore.CYAN + text)

        save_result(text)

        s.close()

    except:

        print(Fore.RED + "Failed.")


# =========================
# SECURITY HEADER SCANNER
# =========================

def security_header_scanner():

    target = input("Enter target URL: ")

    try:

        response = requests.get(target)

        headers = response.headers

        checks = [

            "X-Frame-Options",
            "Content-Security-Policy",
            "Strict-Transport-Security",
            "X-Content-Type-Options"

        ]

        print()

        for header in checks:

            if header in headers:

                text = f"[FOUND] {header}"

                print(Fore.GREEN + text)

                save_result(text)

            else:

                text = f"[MISSING] {header}"

                print(Fore.RED + text)

                save_result(text)

    except:

        print(Fore.RED + "Scan failed")


# =========================
# TECHNOLOGY FINGERPRINTER
# =========================

def technology_fingerprinter():

    target = input("Enter target URL: ")

    try:

        response = requests.get(target)

        headers = response.headers

        print()

        if "Server" in headers:

            text = f"[SERVER] {headers['Server']}"

            print(Fore.GREEN + text)

            save_result(text)

        else:

            print(Fore.RED + "[UNKNOWN SERVER]")

        if "X-Powered-By" in headers:

            text = f"[TECH] {headers['X-Powered-By']}"

            print(Fore.CYAN + text)

            save_result(text)

        else:

            print(Fore.RED + "[TECH UNKNOWN]")

    except:

        print(Fore.RED + "Fingerprint failed")


# =========================
# MENU
# =========================

while True:

    print(Fore.MAGENTA + """

====== RECON FRAMEWORK ======

1. Threaded Port Scanner
2. Directory Scanner
3. Banner Grabber
4. Security Header Scanner
5. Technology Fingerprinter
6. Export JSON Report
7. Exit

=============================

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
        technology_fingerprinter()

    elif choice == "6":
        export_json()

    elif choice == "7":

        print(Fore.RED + "Exiting...")

        break

    else:

        print(Fore.RED + "Invalid option")
