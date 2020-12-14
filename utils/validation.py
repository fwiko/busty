import re
import requests


def target(target):
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?'
        r'\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if re.match(regex, target):
        try:
            requests.head(target, timeout=15)
        except (requests.exceptions.ConnectionError, requests.exceptions.InvalidSchema,
                requests.exceptions.ConnectTimeout):
            print(f'[ERROR] Failed to connect to ({target})')
            return False
        else:
            return True
    else:
        print(f'[ERROR] Invalid target address ({target})')
        return False


"""def status_code(status_code):
    try:
        return int(status_code) in [100,101,102,103,
                                200,201,202,203,204,205,206,207,208,226,
                                300,301,302,303,304,305,306,307,308,
                                400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,421,422,423,424,425,426,428,429,431,451,
                                500,501,502,503,504,505,506,507,508,510,511]
    except ValueError:
        return False"""
