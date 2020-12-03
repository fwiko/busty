import requests, re, sys, argparse, asyncio, aiohttp, datetime

def open_file(filename):
    with open(filename, 'r') as read:
        dictionary = read.read().splitlines()
    return dictionary

def write_output(query):
  
    status_code, url, reason = query['status_code'], query['url'], query['reason']
    if status_code == 200:
        print(f'>>>>> [{status_code}] {url} ({reason}) <<<<<')
    else:
        print(f'[{status_code}] {url} ({reason})')


async def check(session, target):
    async with session.get(target, timeout=15) as response:
        write_output({"url": target, "status_code": response.status, "reason": response.reason})

async def launch_requests(session, target, dictionary, loop):
    await asyncio.gather(
        *[check(session, target.format(payload)) for payload in dictionary],
        return_exceptions=True 
    )

def validate_target(target):
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
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

async def main(loop):

    target = args.target
    dictionary = open_file(args.list)
    link_check = validate_target(target)
    if link_check[0]:
        if target[-1] != '/':
            target = target+'/{}'
        else:
            target = target+'{}'
        async with aiohttp.ClientSession(loop=loop) as session:
            await launch_requests(session, target, dictionary, loop)
    else:
        print(link_check[1])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', help='URL to target', required=True)
    parser.add_argument('--list', help="Specify list of directories to check", required=True)
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))