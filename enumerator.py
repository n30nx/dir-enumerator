from datetime import datetime
from colorama import Fore
from time import perf_counter
import requests
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', action = "store", type = str, required = True, help = "URL or Domain")
    parser.add_argument('--port', action = "store", type = int, required = False, help = "Server's html port that you want to scan, default = 80", default = 80)
    parser.add_argument('--wordlist', action = "store", type = str, required = True, help = "Wordlist's location")
    parser.add_argument('--extensions', action= "store", type = str, required = False, help = "Extensions that you want to scan, deafult = html,php,js", default = "html,php,js")
    parser.add_argument('--ssl', action = "store", type = str, required = False, help = "If website has ssl write enabled, if not write disabled, default = disabled", default = "disabled")
    args = parser.parse_args()
    return args

def get_request(host, port, k, header):
    try:
        req = requests.get(f"{host}:{port}/{k[0]}", headers=header)
        if req.ok:
            print(f"{Fore.RED}[{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}] [*]        {Fore.BLUE}/{k[0]}             {Fore.MAGENTA}size:{len(req.text)}")
        k.pop(0)
    except KeyboardInterrupt:
        exit()
    except:
        pass
        
def main():
    args = parse_args()
    k = args.extensions.split(",")
    l = list()
    p = list()

    if args.ssl == "enabled":
        h = f"https://{args.host}"
    elif args.ssl == "disabled":
        h = f"http://{args.host}"
    else:
        exit()

    header = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Content-Encoding' : 'gzip, deflate, br',
            'Content-Language' : 'en-US;en;q=0.5',
            'Upgrade-Insecure-Requests' : '1',
            'Referer' : h,
            'DNT' : '1',
            'Language' : 'en-US'
    }
    with open(args.wordlist) as f:
        c = f.readlines()
        for i in c:
            i = i.replace("\n", "")
            l.append(i)
            for a in k:
                p.append(i + f".{a}")
        f.close()

    print(f"{Fore.RED}[{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}] [*] {Fore.BLUE}HOST = {Fore.CYAN}{h}")
    print(f"{Fore.RED}[{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}] [*] {Fore.BLUE}PORT = {Fore.CYAN}{args.port}")
    print(f"{Fore.RED}[{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}] [*] {Fore.BLUE}WORDLIST = {Fore.CYAN}{args.wordlist}")
    print(f"{Fore.RED}[{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}] [*] {Fore.BLUE}EXTENSIONS = {Fore.CYAN}{args.extensions}")
    print(f"{Fore.RED}[{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}] [*] {Fore.BLUE}SSL = {Fore.CYAN}{args.ssl}\n\n")

    start = perf_counter()

    for i in range(len(p)):
        if len(l) > 0:
            get_request(h, args.port, l, header)
        get_request(h, args.port, p, header)

    end = perf_counter()
    
    print(f"{Fore.RED}[{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}] [*]{Fore.GREEN} OPERATION COMPLETED IN {end-start} SECONDS{Fore.WHITE}")

if __name__ == "__main__":
    main()
