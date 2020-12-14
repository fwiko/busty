import json
import os
import sys
import argparse
import time
import utils.dirscanner as dirscanner
import utils.validation as validate


def parse_error(message):
    print("Usage: python " + sys.argv[0] + " [Options] use -h for help")
    print("Error: " + message)
    sys.exit()


def parse_args():
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -t example.com -l wordlist.txt")
    parser.error = parse_error
    #parser.add_argument('-m', '--mode', required=True)
    parser.add_argument('-t', '--target', help='Specified target address to scan.', required=True)
    parser.add_argument('-l', '--list', help='Optionally specify a wordlist to use.', required=False)
    #parser.add_argument('-s', '--status', required=False)
    return parser.parse_args()


def transform_target(target):
    return target + '/{}' if target[-1] != '/' else target + '{}'


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
        target = dirscanner.DirScanner(**{
            'target': target,
            'checks': len(words),
            'words': words,
            'config': config
        })
        target.launch()


if __name__ == '__main__':
    arguments = parse_args()

    #if mode == 1 / ds
    if validate.target(arguments.target):
        target = transform_target(arguments.target)
        start_directory_scan(arguments, target)
    
    #if mode == 2 / ps
