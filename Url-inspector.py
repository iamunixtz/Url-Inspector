import argparse
import requests
import ping3
from colorama import init, Fore
import os

def ping_website(website, timeout):
    try:
        response_time = ping3.ping(website, timeout=timeout)
        return response_time is not False
    except PermissionError:
        return False

def check_http_response(website):
    if not website.startswith('http'):
        website = 'http://' + website

    try:
        response = requests.get(website, timeout=10)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def scan_website(website, timeout):
    ping_result = ping_website(website, timeout)
    http_result = check_http_response(website)

    if ping_result and http_result:
        log = f"{website} : 200 : Success"
        print(Fore.GREEN + log)
    elif ping_result and not http_result:
        log = f"{website} : - : HTTP Check Failed"
        print(Fore.RED + log)
    else:
        log = f"{website} : - : Unreachable"
        print(Fore.YELLOW + log)

def scan_websites(filename, timeout):
    try:
        with open(filename, 'r') as file:
            websites = file.readlines()

        for website in websites:
            website = website.strip()
            scan_website(website, timeout)

    except FileNotFoundError:
        print(Fore.RED + "File not found. Please make sure the filename is correct.")

def main(filename, timeout):
    init()

    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen

    banner = r"""
              ,;;;,
             ;;;;;;;
          .-'`\, '/_
        .'   \ ("`(_)
       / `-,.'\ \_/
       \  \/\  `--`
        \  \ \
         / /| |
        /_/ |_|  URL INSPECTOR BY IAMUNIXTZ
       ( _\ ( _\  #:##        #:##        #:##         #:##
                        #:##        #:##        #:##
   """
    print(Fore.CYAN + banner)
    input("Press Enter to start scanning...")
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
    print(Fore.CYAN + banner)
    print("Webping Tool - Scanning Websites")
    print("--------------------------------")
    scan_websites(filename, timeout)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Webping Tool - Scan list of websites")
    parser.add_argument('-s', '--textfile', type=str, metavar='', help='Path to the text file containing websites')
    parser.add_argument('-t', '--timeout', type=int, metavar='', default=15, help='Ping timeout in seconds (default: 15)')

    args = parser.parse_args()
    if args.textfile:
        main(args.textfile, args.timeout)
    else:
        parser.print_help()

