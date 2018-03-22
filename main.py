#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from threds import TorThreadCaller


def main():
    # ./main.py phrase timeout

    # if len(sys.argv) < 2:
    #    exit('Incorrect argument count')

    phrase = 'spisek'  # sys.argv[1].lower()
    tor_instances = 10  # int(sys.argv[2])

    socks_port = 9050  # Default port for Unix Client

    if os.name == 'nt':  # Default port for Windows Client
        socks_port = 9150

    start_url = 'http://54ogum7gwxhtgiya.onion/'  # Greetings for Krang :)

    tor_thread_caller = None
    results = None

    try:
        tor_thread_caller = TorThreadCaller(phrase, start_url, tor_instances)
    except KeyboardInterrupt:
        print 'Searching finished...'
        results = tor_thread_caller.get_results()

    if results is not None:
        print 'Found', len(results), 'results:'
        for url in results:
            print url


if __name__ == '__main__':
    main()
