import socket
import requests
import threading

from stack import Stack
from validation_tools import *
import requests.exceptions as req_ex

stack = None
run_thread = True


class TorThread(threading.Thread):
    def __init__(self, phrase, thread_id):
        threading.Thread.__init__(self)
        self.phrase = phrase
        self.thread_id = thread_id
        self.socks_port = 9050 + thread_id
        self.timeout = 10

    @staticmethod
    def stop():
        global run_thread
        run_thread = False

    def run(self):
        global stack
        global run_thread
        # Waiting for TOR client instance establish connection
        while socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect_ex(('127.0.0.1', self.socks_port)) != 0:
            pass
        # Waiting till at least 1 link is available to process

        url = None
        while url is None:
            url = stack.get_next()

        session = requests.Session()
        session.proxies = {'http': 'socks5h://127.0.0.1:' + str(self.socks_port),
                           'https': 'socks5h://127.0.0.1:' + str(self.socks_port)}

        while run_thread and (url is not None):
            try:
                print 'Thread', self.thread_id, 'processing:', url
                request = session.get(url, timeout=self.timeout)
                current_url = url
                url = stack.get_next()
            except (req_ex.ConnectionError, req_ex.ReadTimeout, req_ex.ConnectTimeout):
                print 'Unable to access site'
                continue

            if not is_mime_correct(request.headers['Content-Type']):
                continue

            content = request.content

            if self.phrase in content.lower():
                stack.add_result(current_url)

            a_href_tuple = get_urls(request.content)

            if a_href_tuple is None:
                continue

            for a_href in a_href_tuple:
                href = a_href['href']
                if is_onion_domain(href) and has_correct_extension(href):
                    stack.add_next(href)


class TorThreadCaller:
    def __init__(self, phrase, start_url, tor_instances):
        global stack

        self.tor_instances = tor_instances
        self.phrase = phrase
        stack = Stack(start_url)

        self.tor_threads = []
        for instance_id in xrange(tor_instances):
            self.tor_threads.append(TorThread(phrase, instance_id))
            self.tor_threads[instance_id].start()

        # Waiting for Ctrl+C
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print 'Searching stopped'

    def get_results(self):
        global stack
        global run_thread
        run_thread = False
        for instance_id in xrange(self.tor_instances):
            self.tor_threads[instance_id].join()
        return stack.get_results()
