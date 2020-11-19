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
    return parser.parse_args()


def start_requesting(url, words):

    for number, word in enumerate(words):
        try:
            req=requests.head(f"{url}/{word.strip()}",timeout=30)
        except Exception as e:
            print(e)
            pass
        else:
            if req.status_code != 404:
                print(f"[{req.status_code}] {url}/{word.strip()}")
    print("\nFinished!")


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
        if (re.match(regex, args.domain) is not None):
            try:
                req = requests.head(args.domain)
                website_check = req.status_code
            except ConnectionError:
                print(f"Failed to connect to '{args.domain}'")
            else:
                start_requesting(args.domain, lines)
        else:
            print("\nError: Invalid domain name")
            print("Usage: python " + sys.argv[0] + " -d https://example.com\n")


if __name__ == "__main__":
    try:
        main(parse_args())
    except KeyboardInterrupt:
        print('goodbye')