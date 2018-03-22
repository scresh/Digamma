#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from threds import TorThreadCaller


def main():
    # ./main.py phrase timeout

    # if len(sys.argv) < 2:
    #    exit('Incorrect argument count')

    phrase = ' '  # sys.argv[1].lower()
    tor_instances = 10  # int(sys.argv[2])

    socks_port = 9050  # Default port for Unix Client

    if os.name == 'nt':  # Default port for Windows Client
        socks_port = 9150

    start_url = 'http://54ogum7gwxhtgiya.onion/'  # Greetings for Krang :)

    results = TorThreadCaller(phrase, start_url, tor_instances).get_results()
    print 'Searching finished...'

    if results is not None:
        print 'Found', len(results), 'results:'
        for url in results:
            print url


if __name__ == '__main__':
    main()
