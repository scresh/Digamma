import time
import requests
import threading
from html2text import html2text
from random import uniform

from stack import Stack
from validation_tools import *
from requests.exceptions import *


stack = None
run_threads = True


class TorThread(threading.Thread):
    def __init__(self, phrase, thread_id, start_port, mode):
        threading.Thread.__init__(self)
        self.phrase = phrase
        self.thread_id = thread_id
        self.socks_port = start_port + thread_id * 2
        self.timeout = 5
        self.mode = mode

    def run(self):
        global stack
        global run_threads

        # Waiting till at least 1 url is available to process
        url = None
        while url is None:
            # Very important line - reduces collisions
            time.sleep(uniform(0, 1))
            url = stack.get_next()

        session = requests.Session()
        session.proxies = {'http': 'socks5h://127.0.0.1:' + str(self.socks_port),
                           'https': 'socks5h://127.0.0.1:' + str(self.socks_port)}

        # Loop can be stopped by:
        #   -> KeyboardInterrupt (Ctrl + C)
        #   -> Stack, if there is no urls to process
        while run_threads and (url is not None):
            try:
                # Race condition only applies to print so it's feature :)
                request = session.get(url, timeout=self.timeout)
                content_type = request.headers['Content-Type']

                content = request.content
                if self.mode == "-f":
                    f = open("test.txt", "a")
                    f.write(url + ":\t" + html2text(content).encode('utf-8').replace("\n", " ").lower() + "\n")
                    f.close()
                elif self.phrase in content.lower():
                    stack.add_result(url)

                urls = get_urls(content, content_type)

                if urls is None:
                    raise Exception('No valid urls')
                else:
                    map(lambda x: stack.add_next(x), urls)
                    raise Exception('Successfully processed')

            except Exception as e:
                thread_str = str(self.thread_id)
                if any(isinstance(e, exc) for exc in (ConnectionError, ReadTimeout, ConnectTimeout)):
                    print 'Thread #' + thread_str + ':\t' + 'Connection error' + ': ' + url
                else:
                    print 'Thread #' + thread_str + ':\t' + str(e) + ': ' + url

                url = stack.get_next()

        # Stop all threads if current thread has no urls to process
        if run_threads:
            run_threads = False


class TorThreadCaller:
    def __init__(self, phrase, start_url, tor_instances, start_port, mode):
        global stack
        global run_threads

        self.tor_instances = tor_instances
        self.phrase = phrase
        stack = Stack(start_url)

        self.tor_threads = []
        for instance_id in xrange(tor_instances):
            self.tor_threads.append(TorThread(phrase, instance_id, start_port, mode))
            self.tor_threads[instance_id].start()

        # Waiting for Ctrl+C
        try:
            while run_threads:
                pass
        except KeyboardInterrupt:
            run_threads = False
            for thread in self.tor_threads:
                thread.join()

    @staticmethod
    def get_results():
        global stack
        return stack.get_results()
