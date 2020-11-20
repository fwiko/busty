import requests, re, sys, argparse
from requests.exceptions import ConnectionError

def parser_error(errmsg):
    print("Usage: python " + sys.argv[0] + "-d https://example.com -w words.txt")
    print("Error: " + errmsg)
    sys.exit()

def parse_args():
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -d https://example.com -w words.txt")
    parser.error = parser_error
    parser.add_argument('-d', '--domain', help="Domain name to check", required=True)
    parser.add_argument('-w', '--words', help="Words list to use", required=True)
    parser.add_argument('-s', '--statuscode', help="Optionally specify a status code to look for", required=False)
    return parser.parse_args()

def start_requesting(url, words, args):
    dirs = 0
    for number, word in enumerate(words):
        try:
            req=requests.head(f"{url}/{word.strip()}",timeout=30)
        except Exception as e:
            print(e)
            pass
        else:
            if req.status_code != 404:
                if args.statuscode:
                    if req.status_code == args.statuscode:
                        print(f"[{req.status_code}] {url}/{word.strip()}")
                        dirs += 1
                else:
                    print(f"[{req.status_code}] {url}/{word.strip()}")
                    dirs += 1

    if dirs > 0:
        print(f"finished | {dirs} directory(s) found")
    else:
        print("finished | nothing found")

def main(args):

    regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    try:
        with open(args.words, 'r') as w:
            lines = w.readlines()
    except Exception as e:
        print("Unable to open/find specified word list")
    else:
        if args.statuscode:
            try:
                if int(args.statuscode) not in [
                                            100,101,102,103,
                                            200,201,202,203,204,205,206,207,208,226,
                                            300,301,302,303,304,305,306,307,308,
                                            400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,421,422,423,424,425,426,428,429,431,451,
                                            500,501,502,503,504,505,506,507,508,510,511
                                        ]:
                    return print("Invalid status code")
                else:
                    args.statuscode = int(args.statuscode)
            except Exception as e:
                return print("Invalid status code")
        if (re.match(regex, args.domain) is not None):
            try:
                req = requests.head(args.domain)
                website_check = req.status_code
            except ConnectionError:
                print(f"Failed to connect to '{args.domain}'")
            else:
                start_requesting(args.domain, lines, args)
        else:
            print("Error: Invalid domain name")
            print("Usage: python " + sys.argv[0] + " -d https://example.com\n")


if __name__ == "__main__":
    try:
        main(parse_args())
    except KeyboardInterrupt:
        print('Exit Program')