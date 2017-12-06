#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import requests.exceptions as req_ex
from BeautifulSoup import BeautifulSoup
from stack import Stack
import signal


def correct(url):
    if url[:4] != 'http':
        return False
    if url.split('/')[2][-6:] != '.onion':
        return False
    return True


def main():
    start_url = 'http://54ogum7gwxhtgiya.onion/'

    session = requests.Session()
    session.proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
    stack = Stack(start_url)

    def signal_handler(signal, frame):
        global interrupted
        interrupted = True

    signal.signal(signal.SIGINT, signal_handler)
    interrupted = False

    while stack.has_next():
        if interrupted:
            break

        url = stack.get_next()
        request = session.get(url, timeout=5)
        if 'text/html' in request.headers['Content-Type']:

            try:
                content = session.get(url, timeout=5).text
            except (req_ex.ConnectionError, req_ex.ReadTimeout):
                print 'Unable to acces site'

        try:
            soup = BeautifulSoup(content)
        except UnicodeEncodeError:
            print 'Invalid HTML file'
            continue

        urls = soup.findAll('a', href=True)

        for u in urls:
            href = u['href']
            if correct(href):
                stack.add_next(href)

        print("Finished!")


if __name__ == '__main__':
    main()
