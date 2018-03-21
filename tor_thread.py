import socket
import requests
import threading
from validation_tools import *
import requests.exceptions as req_ex


class TorThread(threading.Thread):
    def __init__(self, phrase, thread_id):
        threading.Thread.__init__(self)
        self.phrase = phrase
        self.thread_id = thread_id
        self.socks_port = 9050 + thread_id
        self.timeout = 10
        self.results = []

    def run(self, stack):
        # Waiting for TOR client to establish connection
        while socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect_ex(('127.0.0.1', self.socks_port)) != 0:
            pass

        session = requests.Session()
        session.proxies = {'http': 'socks5h://127.0.0.1:' + str(self.socks_port),
                           'https': 'socks5h://127.0.0.1:' + str(self.socks_port)}
        while stack.has_next():
            url = stack.get_next()
            try:
                request = session.get(url, timeout=self.timeout)
            except (req_ex.ConnectionError, req_ex.ReadTimeout, req_ex.ConnectTimeout):
                print 'Unable to access site'
                continue

            if not is_mime_correct(request.headers['Content-Type']):
                continue

            content = request.content

            if self.phrase in content.lower():
                self.results.append(url)

            urls = get_urls(request.content)

            if urls is None:
                continue

            for url in urls:
                href = url['href']
                if is_onion_domain(href) and has_correct_extension(href):
                    stack.add_next(href)
