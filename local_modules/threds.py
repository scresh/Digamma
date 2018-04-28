import time
import requests
import threading
from random import uniform

from stack import Stack
from tools import *
from requests.exceptions import *

TIMEOUT = 5
stack = None
run_threads = True
file_lock = threading.Lock()


class TorThread(threading.Thread):
    def __init__(self, thread_id, start_port, output_file, words):
        threading.Thread.__init__(self)
        self.words = words
        self.thread_id = thread_id
        self.socks_port = start_port + thread_id * 2
        self.output_file = output_file

    def run(self):
        global stack
        global run_threads
        global file_lock

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

        # Run phrase-search mode
        if self.words is not None:
            while run_threads and (url is not None):
                try:
                    # Race condition only applies to print so it's feature :)
                    request = session.get(url, timeout=TIMEOUT)
                    content_type = request.headers['Content-Type']
                    if not is_mime_correct(content_type):
                        raise Exception('Incorrect content type')

                    content = request.content
                    if all(word in content.lower() for word in self.words):
                        stack.add_result(url)
                        file_lock.acquire()
                        self.output_file.write(url + '\n')
                        file_lock.release()

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
            # Run harvest mode
        else:
            while run_threads and (url is not None):
                try:
                    # Race condition only applies to print so it's feature :)
                    request = session.get(url, timeout=TIMEOUT)
                    content_type = request.headers['Content-Type']
                    if not is_mime_correct(content_type):
                        raise Exception('Incorrect content type')

                    content = request.content
                    words = get_words(content)
                    file_lock.acquire()
                    self.output_file.insert(url, words)
                    file_lock.release()

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
    def __init__(self, start_url, threads, start_port, output_file, words):
        global stack
        global run_threads
        stack = Stack(start_url)

        self.tor_threads = []
        for thread_id in xrange(threads):
            self.tor_threads.append(TorThread(thread_id, start_port, output_file, words))
            self.tor_threads[thread_id].start()

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
