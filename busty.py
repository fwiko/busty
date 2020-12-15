import json
import os
import sys
import argparse
import time
import utils.scanner as scanner
import utils.validation as validate


def parse_error(message):
    print("Usage: python " + sys.argv[0] + " [Options] use -h for help")
    print("Error: " + message)
    sys.exit()


def parse_args():
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -t example.com -l wordlist.txt")
    parser.error = parse_error
    parser.add_argument('-m', '--mode', help='Select the mode to run (ds, ss)', required=True)
    parser.add_argument('-t', '--target', help='Specified target address to scan.', required=True)
    parser.add_argument('-l', '--list', help='Optionally specify a wordlist to use.', required=False)
    #parser.add_argument('-s', '--status', required=False)
    return parser.parse_args()


def ds_transform_target(target):
    return target + '/{}' if target[-1] != '/' else target + '{}'


def ss_transform_target(target):
    url = target.split("/")
    url[2] = '{}.' + url[2]
    return '/'.join(url)


def start_directory_scan(args, target):
    try:
        config = json.load(open('config.json', 'r'))['dirscanner']
    except FileNotFoundError:
        print('[ERROR] Config file could not be found')
    else:
        if not args.list:
            try:
                words = open('wordlists/default.txt', 'r').read().splitlines()
                print('[BUSTY] Using default.txt')
                time.sleep(1.5)
            except FileNotFoundError:
                print('[ERROR] Default wordlist cannot be found., please specify a wordlist.')
                sys.exit()
        else:
            try:
                words = open('wordlists/'+args.list, 'r').read().splitlines()
                print(f'[BUSTY] Using {args.list}')
                time.sleep(1.5)
            except FileNotFoundError:
                print('[ERROR] Specified wordlist cannot be found.')
                sys.exit()
        target = scanner.Browse(**{
            'target': target,
            'words': words,
            'config': config
        })
        target.launch()


if __name__ == '__main__':
    arguments = parse_args()

    if arguments.mode == '1' or arguments.mode == 'ds':
        if validate.target(arguments.target):
            target = ds_transform_target(arguments.target)
            start_directory_scan(arguments, target)
    """elif arguments.mode == '2' or arguments.mode == 'ss':
        if validate.target(arguments.target):
            target = ss_transform_target(arguments.target)
            start_subdirectory_scan(arguments, target)"""