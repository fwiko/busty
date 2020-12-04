import requests
import re
import sys
import argparse
import asyncio
import aiohttp
import time
from datetime import date


def open_file(filename):
    with open(filename, 'r') as read:
        dictionary = read.read().splitlines()
    return dictionary


def output_to_file(title):
    with open(f'{title}-[{date.today()}].txt', 'a') as log:
        for result in results:
            log.write(f'[{result[0]}] {result[1]}\n')
        log.close()


async def write_output(query):
    status_code = query['status_code']
    url = query['url']
    if args.status:
        if status_code == int(args.status):
            results.append([status_code, url])
            print(f'[{status_code}] {url}')
    else:
        results.append([status_code, url])
        print(f'[{status_code}] {url}')


async def check(session, target):
    async with session.get(target, timeout=15) as response:
        await write_output({
            "url": target,
            "status_code": response.status,
            })


async def launch_requests(session, target, dictionary, loop):
    try:
        await asyncio.gather(
            *[check(session, target.format(payload)) for payload in dictionary],
            return_exceptions=True
        )
    except KeyboardInterrupt:
        output_to_file(target.split('/')[2])
    else:
        output_to_file(target.split('/')[2])


def validate_target(target):
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?'
        r'\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if (re.match(regex, target)):
        try:
            requests.head(target)
        except requests.exceptions.ConnectionError:
            return [False, f'Failed to connect to [{target}]']
        return [True]
    else:
        return [False, f'Invalid link [{target}]']


def validate_status_code(status_code):
    try:
        if int(status_code) in [100,101,102,103,
                                200,201,202,203,204,205,206,207,208,226,
                                300,301,302,303,304,305,306,307,308,
                                400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,421,422,423,424,425,426,428,429,431,451,
                                500,501,502,503,504,505,506,507,508,510,511]:
            return True
        else:
            return False
    except ValueError:
        return False


async def main(loop):

    target = args.target
    dictionary = open_file(args.list)
    link_check = validate_target(target)
    if args.status:
        status_check = validate_status_code(args.status)
    else:
        status_check = True

    if link_check[0]:
        if status_check:
            if target[-1] != '/':
                target = target+'/{}'
            else:
                target = target+'{}'
            async with aiohttp.ClientSession(loop=loop) as session:
                await launch_requests(session, target, dictionary, loop)
            print(f'Finished in {round(time.time()-start_time, 2)} seconds')
        else:
            print(f'Invalid status code [{args.status}]')
    else:
        print(link_check[1])

if __name__ == '__main__':
    results = []
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', help='URL to target', required=True)
    parser.add_argument(
        '--list', help="Specify list of directories to check",
        required=True)
    parser.add_argument(
        '-s',
        '--status',
        help="Optionally specify a status code to look for",
        required=False)
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
