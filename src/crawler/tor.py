import os

import argparse
import requests
import threading

from time import sleep
from tools import methods
from random import uniform
from getpass import getpass
from tools.shared_memory import TorSharedMemory


class TorThread(threading.Thread):
    def __init__(self, thread_id, shared_memory):
        super().__init__()
        self.thread_id = thread_id

        socks_port = shared_memory.start_port + 2 * thread_id

        self.proxies = {'http': 'socks5h://127.0.0.1:' + str(socks_port),
                        'https': 'socks5h://127.0.0.1:' + str(socks_port)}

        self.shared_memory = shared_memory

    def run(self):

        while self.shared_memory.run_threads:
            try:
                requests.get(
                    'http://www.google.com/',
                    timeout=self.shared_memory.timeout,
                    proxies=self.proxies
                )
            except requests.ConnectTimeout:
                self.print(f'Attempting to establish Tor connection: Waiting...', methods.NORMAL)
                sleep(1)
                continue
            else:
                break

        while self.shared_memory.run_threads:

            url = self.shared_memory.get_url(self.thread_id)

            if url is None:
                if self.shared_memory.any_active():
                    sleep(uniform(0, 1))
                    self.print(f'Attempting to get new url: Waiting...', methods.NORMAL)
                    continue
                else:
                    self.shared_memory.run_threads = False
                    self.print(f'No urls to process: Stop all threads', methods.WARNING)
                    break

            try:
                request = requests.get(
                    url,
                    timeout=self.shared_memory.timeout,
                    proxies=self.proxies
                )
                content_type = request.headers['Content-Type']
                if not methods.is_mime_correct(content_type):
                    raise IncorrectContentType

                content = request.content
                if all(word in content.lower() for word in self.shared_memory.phrase_words):
                    if self.shared_memory.db_mode():
                        title = methods.get_title(content)
                        plain = methods.get_plain(content)
                        words = methods.get_words(plain)
                        sentences = methods.get_sentences(plain)
                        self.shared_memory.save_page(url, words, content, title, sentences)

                    self.shared_memory.save_url(url)

                urls = methods.get_urls(url, content, content_type)

                if urls:
                    for x in urls:
                        self.shared_memory.add_url(x)
                else:
                    raise NoURLsFound

            except Exception as e:
                self.print(f'{type(e).__name__}: {url}', methods.WARNING)
            else:
                self.print(f'Successfully processed: {url}', methods.SUCCESS)

            self.shared_memory.set_inactive(self.thread_id)

    def print(self, text, color):
        if self.shared_memory.run_threads:
            print(f'Thread #{self.thread_id}:\t{color}{text}{methods.NORMAL}')


def main():
    parser = argparse.ArgumentParser(description='Run Tor scanner for a given phrase')
    parser.add_argument("--save", help="Save all matching results to .db file", action="store_true")
    parser.add_argument('--phrase', help='Space separated word list')
    parser.add_argument('--threads', type=int, default=4, choices=range(1, 64), help='The number of threads')
    parser.add_argument('--port', type=int, choices=range(1024, 65535), help='The custom port zero')
    parser.add_argument('--url', help='The first page url')
    args = parser.parse_args()

    if os.name == 'nt':
        start_port = 9150
    else:
        start_port = 9050
        root_password = getpass(prompt="Enter root password: ")

        if methods.execute('dpkg -l tor') != 0:
            methods.execute(f'yes | echo {root_password} | sudo -S apt-get install tor')

        methods.execute(f'echo {root_password} | sudo -S service tor stop')
        methods.execute('rm -rf /tmp/digamma/ && mkdir /tmp/digamma/')

    if args.port:
        start_port = args.port

    phrase_words = []
    if args.phrase:
        phrase_words = args.phrase.split()

    start_url = 'http://54ogum7gwxhtgiya.onion/'  # Greetings for Krang :)
    if args.url:
        start_url = args.url

    thread_list = []
    shared_memory = TorSharedMemory(phrase_words, start_port, timeout=5, save_mode=args.save, threads_no=args.threads)
    shared_memory.add_url(start_url)

    for thread_id in range(args.threads):
        start_cmd = f'tor' \
            f' --SocksPort {start_port + 2 * thread_id}' \
            f' --ControlPort {start_port + 2 * thread_id + 1}' \
            f' --DataDirectory /tmp/digamma/{start_port + 2 * thread_id}' \
            f' --RunAsDaemon 1'
        methods.execute(start_cmd)

        thread_list.append(TorThread(thread_id, shared_memory))
        thread_list[thread_id].start()

    # Waiting for Ctrl+C
    try:
        while shared_memory.run_threads:
            sleep(0.25)
    except KeyboardInterrupt:
        print(f'\nStopping {args.threads} threads...')
        shared_memory.run_threads = False
        for thread in thread_list:
            thread.join()


if __name__ == '__main__':
    main()


class NoURLsFound(Exception):
    pass


class IncorrectContentType(Exception):
    pass
