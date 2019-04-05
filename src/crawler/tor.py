import os

import argparse
import requests
import threading

from time import sleep
from tools import methods
from random import uniform
from getpass import getpass

from tools.db import Database
from tools.shared_memory import TorSharedMemory


class NoURLsFound(Exception):
    pass


class IncorrectContentType(Exception):
    pass


class TorThread(threading.Thread):
    def __init__(self, thread_id, shared_memory):
        super().__init__()
        self.thread_id = thread_id

        socks_port = shared_memory.start_port + 2 * thread_id

        self.proxies = {'http': 'socks5h://127.0.0.1:' + str(socks_port),
                        'https': 'socks5h://127.0.0.1:' + str(socks_port)}

        self.shared_memory = shared_memory
        self.thread_memory = []

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

                if 'text/html' not in request.headers['Content-Type']:
                    raise IncorrectContentType

                html = request.text

                title, content, words, urls = methods.get_values(html, url)

                self.thread_memory.append((title, content, words, url))

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
            thread_id_str = str(self.thread_id).zfill(3)
            print(f'[ Thread #{thread_id_str} ]\t{color}{text}{methods.NORMAL}')


def main():
    parser = argparse.ArgumentParser(description='Run Tor scanner')
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

    start_url = 'http://54ogum7gwxhtgiya.onion/'  # Greetings for Krang :)
    if args.url:
        start_url = args.url

    thread_list = []
    db_file = Database()
    shared_memory = TorSharedMemory(start_port, timeout=5, threads_no=args.threads)
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
        shared_memory.run_threads = False
        print(f'\nStopping {args.threads} threads...')

    for thread in thread_list:
        thread_id_str = str(thread.thread_id).zfill(3)
        print(f'[ Thread #{thread_id_str} ]\t Saving pages...')
        db_file.insert_pages(thread.thread_memory)
        thread.join()


if __name__ == '__main__':
    main()


