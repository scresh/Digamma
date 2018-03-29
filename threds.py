import time
import sys
import requests
import threading
from html2text import html2text
from random import uniform
from stack import Stack
from validation_tools import *
from requests.exceptions import *

reload(sys)
sys.setdefaultencoding('utf8')

stack = None
run_threads = True


class TorThread(threading.Thread):
    def __init__(self, phrase, thread_id, start_port, mode):
        threading.Thread.__init__(self)
        self.phrase = phrase
        self.mode = mode
        self.thread_id = thread_id
        self.socks_port = start_port + thread_id * 2
        self.timeout = 5

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

                # Prevent processing images, videos, etc.
                if not is_mime_correct(request.headers['Content-Type']):
                    raise Exception('Incorrect Content-Type')

                content = request.content

                if self.mode == "-f":
                    f = open("test.txt", "a")
                    f.write(url + ":\t" + html2text(content).encode('utf-8').replace("\n"," ").lower() + "\n")
                    f.close()
                else:
                    if self.phrase in content.lower():
                        stack.add_result(url)

                a_href_tuple = get_urls(request.content)
                if a_href_tuple is None:
                    raise Exception('No valid urls')

                for a_href in a_href_tuple:
                    href = a_href['href']
                    if is_onion_domain(href) and has_correct_extension(href):
                        stack.add_next(href)
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
        self.mode = mode
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
