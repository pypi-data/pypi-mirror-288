import shutil
import datetime
import platform
import string
import time
import random
import os
import sys

try:
    import requests
    from cfonts import render
except ModuleNotFoundError:
    os.system('pip install requests')
    os.system('pip install python-cfonts')
    os.system('clear')

columns = shutil.get_terminal_size().columns

def logo():
    os.system('clear')
    logo = render("TN WARP", colors=["red", "black"], align="center")
    print(logo)
    print()

class Color:
    LIGHT_BLACK = '\033[90m'
    LIGHT_RED = '\033[91m'
    LIGHT_GREEN = '\033[92m'
    LIGHT_YELLOW = '\033[93m'
    LIGHT_BLUE = '\033[94m'
    LIGHT_MAGENTA = '\033[95m'
    LIGHT_CYAN = '\033[96m'
    LIGHT_WHITE = '\033[97m'
    RESET_ALL = '\033[0m'

def write(z, end="\n"):
    for e in z + end:
        sys.stdout.write(e)
        sys.stdout.flush()
        time.sleep(0.02)

def clear():
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    logo()

def success(m):
    localTime = time.localtime()
    current_time = time.strftime("%I:%M:%S", localTime)
    print((f"\r\033[92m    [\033[94m {current_time} \033[92m] WARP MB Sent : \033[94m[\033[37m{m} GB\033[94m]\033[37m").center(columns), end="")

def gen_string(string_length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(string_length))

def digit_string(string_length):
    digits = string.digits
    return ''.join(random.choice(digits) for _ in range(string_length))

url = f'https://api.cloudflareclient.com/v0a{digit_string(3)}/reg'

def run(referrer):
    try:
        install_id = gen_string(22)
        body = {
            "key": "{}=".format(gen_string(43)),
            "install_id": install_id,
            "fcm_token": "{}:APA91b{}".format(install_id, gen_string(134)),
            "referrer": referrer,
            "warp_enabled": False,
            "tos": datetime.datetime.now().isoformat()[:-3] + "+02:00",
            "type": "Android",
            "locale": "es_ES"
        }
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Host': 'api.cloudflareclient.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.12.1'
        }
        response = requests.post(url, json=body, headers=headers)
        return response.status_code
    except Exception as error:
        return None

def getReferrer():
    referr = input(f"    {Color.LIGHT_GREEN}[{Color.LIGHT_WHITE}*{Color.LIGHT_GREEN}]{Color.RESET_ALL} Enter Your WARP ID {Color.LIGHT_RED}=> {Color.RESET_ALL} ")
    if referr == '':
        write(f"\n    {Color.LIGHT_GREEN}[{Color.LIGHT_RED}!{Color.LIGHT_GREEN}] {Color.LIGHT_RED}Please Enter a Correct WARP ID {Color.LIGHT_GREEN}!{Color.RESET_ALL}")
        time.sleep(1.5)
        clear()
        referr = getReferrer()

    return referr

def tnwarp(o):
    if o != 'rohit' or o == "":
        print(f'{Color.LIGHT_RED}Warning: The provided argument is not recognized. It must be "rohit"{Color.RESET_ALL}')
        return

    logo()
    ref = getReferrer()
    print('\n\n')

    s = 0

    while True:
        result = run(ref)
        if result == 200:
            s += 1
        success(s)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f'{Color.LIGHT_RED}Error: You must provide exactly one argument: "rohit"{Color.RESET_ALL}')
        sys.exit(1)
    tnwarp(sys.argv[1])