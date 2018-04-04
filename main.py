#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from threds import TorThreadCaller


def main():
    # Default values
    phrase = 'conspiracy'
    tor_instances = 1
    mode = ""
    start_url = 'http://54ogum7gwxhtgiya.onion/'  # Greetings for Krang :)

    if len(sys.argv) > 1:
        phrase = sys.argv[1]
    if len(sys.argv) > 2:
        tor_instances = int(sys.argv[2])
    if len(sys.argv) > 3:
        mode = sys.argv[3]

    start_port = [9050, 9150][os.name == 'nt']  # Default ports for Unix and Windows Clients

    results = TorThreadCaller(phrase, start_url, tor_instances, start_port, mode).get_results()
    print 'Searching finished...'

    if results is not None:
        print 'Found', len(results), 'results:'
        for url in results:
            print url


if __name__ == '__main__':
    main()
