#!/usr/bin/env python
# -*- coding: utf-8 -*-

from stack import Stack
from validation_tools import *

import requests
import requests.exceptions as req_ex
import os


def main():
    socks_port = '9050'  # Default port for Unix Client
    request_timeout = 10

    if os.name == 'nt':  # Default port for Windows Client
        socks_port = '9150'

    session = requests.Session()
    session.proxies = {'http': 'socks5h://127.0.0.1:' + socks_port,
                       'https': 'socks5h://127.0.0.1:' + socks_port}

    start_url = 'http://54ogum7gwxhtgiya.onion/'  # Greetings for Krang :)
    stack = Stack(start_url)
    try:
        while stack.has_next():
            url = stack.get_next()
            try:
                request = session.get(url, timeout=request_timeout)
            except (req_ex.ConnectionError, req_ex.ReadTimeout, req_ex.ConnectTimeout):
                continue
                print 'Unable to access site'

            if not is_mime_correct(request.headers['Content-Type']):
                continue

            urls = get_urls(request.content)

            if urls is None:
                continue

            for url in urls:
                href = url['href']
                if is_onion_domain(href):
                    stack.add_next(href)
    except KeyboardInterrupt:
        print 'Zakonczono!'


if __name__ == '__main__':
    main()
