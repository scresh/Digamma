#!/usr/bin/env python
# -*- coding: utf-8 -*-

from stack import Stack
from validation_tools import *

import requests
import requests.exceptions as req_ex

import sys
import os


def main():
    # ./main.py phrase timeout

    if len(sys.argv) < 2:
        print 'Incorrect argument count'
        return
    phrase = sys.argv[1].lower()

    try:
        request_timeout = int(sys.argv[2])
    except (IndexError, IndexError):
        request_timeout = 5

    socks_port = '9050'  # Default port for Unix Client

    if os.name == 'nt':  # Default port for Windows Client
        socks_port = '9150'

    session = requests.Session()
    session.proxies = {'http': 'socks5h://127.0.0.1:' + socks_port,
                       'https': 'socks5h://127.0.0.1:' + socks_port}

    start_url = 'http://54ogum7gwxhtgiya.onion/'  # Greetings for Krang :)
    stack = Stack(start_url)

    phrase_results = []

    try:
        while stack.has_next():
            url = stack.get_next()
            try:
                request = session.get(url, timeout=request_timeout)
            except (req_ex.ConnectionError, req_ex.ReadTimeout, req_ex.ConnectTimeout):
                print 'Unable to access site'
                continue

            if not is_mime_correct(request.headers['Content-Type']):
                continue

            content = request.content

            if phrase in content.lower():
                phrase_results.append(url)

            urls = get_urls(request.content)

            if urls is None:
                continue

            for url in urls:
                href = url['href']
                if is_onion_domain(href) and has_correct_extension(href):
                    stack.add_next(href)

    except KeyboardInterrupt:
        print 'Searching finished...'

    print 'Found', len(phrase_results), 'results:'
    for url in phrase_results:
        print url


if __name__ == '__main__':
    main()
