from threading import Lock
from datetime import datetime
from .db import TorDatabase


class SharedMemory:
    def __init__(self, phrase_words, start_port, timeout, save_mode, threads_no):
        self.phrase_words = phrase_words
        self.start_port = start_port
        self.timeout = timeout
        self.run_threads = True

        filename = datetime.now().strftime("%Y-%m-%d %H_%M_%S")
        self._txt_file = open(filename + '.txt', 'w+')
        self._db_file = TorDatabase(f'../db-server/db/{filename}.db') if save_mode else None

        self._index = 0
        self._url_stack = []
        self._threads_active = [False] * threads_no

        self._url_stack_lock = Lock()
        self._txt_file_lock = Lock()
        self._db_file_lock = Lock()

    def add_url(self, url):
        self._url_stack_lock.acquire()
        if url not in self._url_stack:
            self._url_stack.append(url)
        self._url_stack_lock.release()

    def get_url(self, thread_id):
        self._url_stack_lock.acquire()

        if self._index >= len(self._url_stack):
            self._url_stack_lock.release()
            return None

        url = self._url_stack[self._index]
        self._index += 1
        self._threads_active[thread_id] = True

        self._url_stack_lock.release()
        return url

    def save_url(self, url):
        self._txt_file_lock.acquire()
        self._txt_file.write(url + '\n')
        self._txt_file_lock.release()

    def save_page(self, url, words, content, title, sentences):
        if self._db_file:
            self._db_file_lock.acquire()
            self._db_file.insert(url, words, content, title, sentences)
            self._db_file_lock.release()

    def db_mode(self):
        return True if self._db_file else False

    def any_active(self):
        return any(self._threads_active)

    def set_inactive(self, thread_id):
        self._threads_active[thread_id] = False
