#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import requests
import threading

from time import sleep
from tools import tools
from random import uniform
from getpass import getpass
from tools.urlstack import SharedMemory
from requests import ConnectionError, ReadTimeout, ConnectTimeout


class TorThread(threading.Thread):
    def __init__(self, thread_id, shared_memory):
        threading.Thread.__init__(self)
        self.thread_id = thread_id

        socks_port = shared_memory.start_port + 2 * thread_id

        self.session = requests.Session()
        self.session.proxies = {'http': 'socks5h://127.0.0.1:' + str(socks_port),
                                'https': 'socks5h://127.0.0.1:' + str(socks_port)}

        self.shared_memory = shared_memory

    def run(self):

        while self.shared_memory.run_threads:
            url = self.shared_memory.get_url(self.thread_id)

            if url is None:
                if self.shared_memory.any_active():
                    sleep(uniform(0, 1))
                    continue
                else:
                    self.shared_memory.run_threads = False
                    break

            try:
                request = self.session.get(url, timeout=self.shared_memory.timeout)
                content_type = request.headers['Content-Type']
                if not tools.is_mime_correct(content_type):
                    raise Exception('Incorrect content type')

                content = request.content
                if all(word in content.lower() for word in self.shared_memory.phrase_words):
                    if self.shared_memory.db_mode():
                        title = tools.get_title(content)
                        plain = tools.get_plain(content)
                        words = tools.get_words(plain)
                        sentences = tools.get_sentences(plain)
                        self.shared_memory.save_page(url, words, content, title, sentences)

                    self.shared_memory.save_url(url)

                urls = tools.get_urls(url, content, content_type)
                if not urls:
                    raise Exception('No valid urls')
                else:
                    map(lambda x: self.shared_memory.add_url(x), urls)
                    raise Exception('Successfully processed')

            except Exception as e:
                thread_str = str(self.thread_id)
                if any(isinstance(e, exc) for exc in (ConnectionError, ReadTimeout, ConnectTimeout)):
                    print 'Thread #' + thread_str + ':\t' + 'Connection error' + ': ' + url
                else:
                    print 'Thread #' + thread_str + ':\t' + str(e) + ': ' + url

            self.shared_memory.set_inactive(self.thread_id)


def main():
    parser = argparse.ArgumentParser(description='Run Tor scanner for a given phrase')
    parser.add_argument("--save", help="Save all matching results to .db file", action="store_true")
    parser.add_argument('--phrase', help='Space separated word list')
    parser.add_argument('--threads', type=int, default=4, choices=xrange(1, 64), help='The number of threads')
    parser.add_argument('--port', type=int, choices=xrange(1024, 65535), help='The custom port zero')
    parser.add_argument('--url', help='The first page url')
    args = parser.parse_args()

    root_password = getpass(prompt="Enter root password:")

    # Check if tor is installed
    if os.system('dpkg -l | grep torsocks > /dev/null') != 0:
        os.system('yes | echo {} | sudo -S apt-get install tor'.format(root_password))
    else:
        os.system('echo {} | sudo -S service tor stop'.format(root_password))

    os.system('rm -rf /tmp/digamma/ && mkdir /tmp/digamma/')

    start_port = [9050, 9150][os.name == 'nt']  # Default ports for Unix and Windows Clients
    if args.port:
        start_port = args.port

    phrase_words = []
    if args.phrase:
        phrase_words = args.phrase.split()

    start_url = 'http://54ogum7gwxhtgiya.onion/'  # Greetings for Krang :)
    if args.url:
        start_url = args.url

    thread_list = []
    shared_memory = SharedMemory(phrase_words, start_port, timeout=5, save_mode=args.save, threads_no=args.threads)
    shared_memory.add_url(start_url)

    for thread_id in xrange(args.threads):
        os.system(
            'tor --SocksPort {} --ControlPort {} --DataDirectory "/tmp/digamma/{}"  --quiet &'.format(
                start_port + 2 * thread_id,
                start_port + 2 * thread_id + 1,
                start_port + 2 * thread_id,
            )
        )

        while os.system('! nc -z localhost {}'.format(start_port + 2 * thread_id)) == 0:
            sleep(0.2)

        thread_list.append(TorThread(thread_id, shared_memory))
        thread_list[thread_id].start()

    # Waiting for Ctrl+C
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        shared_memory.run_threads = False
        for thread in thread_list:
            thread.join()


if __name__ == '__main__':
    main()
