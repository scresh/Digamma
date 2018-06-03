#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from sys import argv, exit
from datetime import datetime
from local_modules.db import TorDatabase
from local_modules.threds import TorThreadCaller

MAX_THREADS = 32

PARAMS = {
    'threads': ('--threads', '-t'),
    'output': ('--output', '-o'),
    'words': ('--words', '-w'),
    'port': ('--port', '-p'),
    'url': ('--url', '-u'),
}


def main():
    # Default values
    start_port = [9050, 9150][os.name == 'nt']  # Default ports for Unix and Windows Clients
    start_url = 'http://54ogum7gwxhtgiya.onion/'  # Greetings for Krang :)
    filename = datetime.now().strftime("%Y-%m-%d %H_%M_%S")
    output_file = None
    threads = 1
    words = None
    results = None

    # Parse arguments
    for i in xrange(1, len(argv) - 1):
        if argv[i] in PARAMS['threads']:
            try:
                arg = int(argv[i + 1])
            except ValueError:
                exit('--threads value must be a number')
            if arg < 1:
                exit('--threads value must be a positive')
            if arg > MAX_THREADS:
                exit('--threads value must not be greater than %d' % MAX_THREADS)
            threads = arg

        elif argv[i] in PARAMS['output']:
            filename = argv[i + 1]

        elif argv[i] in PARAMS['words']:
            words = argv[i + 1].lower().split()

        elif argv[i] in PARAMS['port']:
            try:
                arg = int(argv[i + 1])
            except ValueError:
                exit('--port value must be a number')
            if arg < 1 or arg > 2 ** 16 - 1:
                exit('--port value must be within the range 1 and 65535')
        elif argv[i] in PARAMS['url']:
            start_url = argv[i + 1]

    try:
        if words is None:
            filename = filename + '.db'
            output_file = TorDatabase(filename)
        else:
            filename = filename + '.txt'
            output_file = open(filename, 'w')
    except Exception:
        exit('Can not write to file: %s' % filename)
    try:
        results = TorThreadCaller(start_url, threads, start_port, output_file, words).get_results()
    except KeyboardInterrupt:
        pass
    print 'Searching finished...'

    if results is not None:
        print 'Found', len(results), 'results:'
        for url in results:
            print url


if __name__ == '__main__':
    main()
