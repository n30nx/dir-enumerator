from typing import List, Dict
from time import perf_counter
from datetime import datetime
from colorama import Fore

import requests
import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', action="store", type=str, required=True, help="URL or Domain")

    parser.add_argument('--port', action="store", type=int, required=False,
        help="Server's html port that you want to scan, default=80", default=80)

    parser.add_argument('--wordlist', action="store", type=str, required=True, help="Wordlist's location")

    parser.add_argument('--extensions', action="store", type=str, required=False,
        help = "Extensions that you want to scan, deafult=html,php,js", default="html,php,js")

    parser.add_argument('--ssl', action="store", type=str, required=False,
        help = "If website has ssl write enabled, if not write disabled, default = disabled", default="disabled")

    args = parser.parse_args()
    return args


def print_log(color: Fore, message: str, color2: Fore, message2: str) -> None:
    now = datetime.now()
    format_time = lambda time: str(time).zfill(2)
    hour = format_time(now.hour)
    minute = format_time(now.minute)
    second = format_time(now.second)
    print(f"{Fore.RED}[{hour}:{minute}:{second}] [*] {color}{message}{color2}{message2}")


def get_request(host: str, port: int, files: List[str], header: Dict[str, str]) -> None:
    try:
        req = requests.get(f"{host}:{port}/{files[0]}", headers=header)
        if req.ok:
            print_log(Fore.BLUE, f"/{files[0]}\t", Fore.MAGENTA, f"size: {len(req.text)}")
        files.pop(0)
    except KeyboardInterrupt:
        exit()
    except:
        pass


def main() -> None:
    args = parse_args()
    extensions = args.extensions.split(",")
    dirs = list()
    files = list()

    if args.ssl == "enabled":
        host = f"https://{args.host}"
    elif args.ssl == "disabled":
        host = f"http://{args.host}"
    else:
        exit(1)

    header = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Content-Encoding' : 'gzip, deflate, br',
            'Content-Language' : 'en-US;en;q=0.5',
            'Upgrade-Insecure-Requests' : '1',
            'Referer' : host,
            'DNT' : '1',
            'Language' : 'en-US'
    }

    with open(args.wordlist) as file:
        content = file.readlines()
        for line in content:
            line = line.replace("\n", "")
            dirs.append(line)
            for extension in extensions:
                files.append(line + f".{extension}")

    print_log(Fore.BLUE, "HOST=", Fore.CYAN, host)
    print_log(Fore.BLUE, "PORT=", Fore.CYAN, args.port)
    print_log(Fore.BLUE, "WORDLIST=", Fore.CYAN, args.wordlist)
    print_log(Fore.BLUE, "EXTENSIONS=", Fore.CYAN, args.extensions)
    print_log(Fore.BLUE, "SSL=", Fore.CYAN, f"{args.ssl}\n\n")

    start = perf_counter()

    for i in range(len(files)):
        if len(dirs) > 0:
            get_request(host, args.port, dirs, header)
        get_request(host, args.port, files, header)

    end = perf_counter()

    print("\n")
    print_log(Fore.GREEN, f"OPERATION COMPLETED IN {end-start} SECONDS", Fore.WHITE, "")


if __name__ == "__main__":
    main()
