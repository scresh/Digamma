import socket
import requests
import threading

from stack import Stack
from validation_tools import *
import requests.exceptions as req_ex

stack = None
run_threads = True


class TorThread(threading.Thread):
    def __init__(self, phrase, thread_id):
        threading.Thread.__init__(self)
        self.phrase = phrase
        self.thread_id = thread_id
        self.socks_port = 9050 + thread_id
        self.timeout = 10

    def run(self):
        global stack
        global run_threads

        # Waiting for TOR client instance establish connection
        while socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect_ex(('127.0.0.1', self.socks_port)) != 0:
            pass

        # Waiting till at least 1 url is available to process
        url = None
        while url is None:
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
                print self.thread_id
                request = session.get(url, timeout=self.timeout)
            except (req_ex.ConnectionError, req_ex.ReadTimeout, req_ex.ConnectTimeout):
                print 'Unable to access site', url
                url = stack.get_next()
                continue

            # Prevent processing images, videos, etc.
            if not is_mime_correct(request.headers['Content-Type']):
                url = stack.get_next()
                continue
            content = request.content

            if self.phrase in content.lower():
                stack.add_result(url)

            a_href_tuple = get_urls(request.content)

            if a_href_tuple is None:
                url = stack.get_next()
                continue

            for a_href in a_href_tuple:
                href = a_href['href']
                if is_onion_domain(href) and has_correct_extension(href):
                    stack.add_next(href)

        # Stop all threads if current thread has no urls to process
        if run_threads:
            run_threads = False


class TorThreadCaller:
    def __init__(self, phrase, start_url, tor_instances):
        global stack
        global run_threads

        self.tor_instances = tor_instances
        self.phrase = phrase
        stack = Stack(start_url)

        self.tor_threads = []
        for instance_id in xrange(tor_instances):
            self.tor_threads.append(TorThread(phrase, instance_id))
            self.tor_threads[instance_id].start()

        # Waiting for Ctrl+C
        try:
            while run_threads:
                pass
        except KeyboardInterrupt:
            run_threads = False

        for instance_id in xrange(self.tor_instances):
            self.tor_threads[instance_id].join()

    @staticmethod
    def get_results():
        global stack
        return stack.get_results()
