from random import randint
from threading import Lock


class IoTSharedMemory:
    def __init__(self, threads_no, ports, timeout, file):
        self.threads_no = threads_no
        self.timeout = timeout
        self.ports = ports
        self.run_threads = True
        self.socket_list = None

        self.seed = randint(0, 256**4-1)

        if file:
            self.socket_list = [*map(lambda x: (
                x.split(':')[0], int(x.split(':')[1])),
                file.read().strip().split('\n')
            )]


class TorSharedMemory:
    def __init__(self, start_port, timeout, threads_no):
        self.start_port = start_port
        self.timeout = timeout
        self.run_threads = True

        self._index = 0
        self._url_stack = []
        self._threads_active = [False] * threads_no

        self._url_stack_lock = Lock()

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

    def any_active(self):
        return any(self._threads_active)

    def set_inactive(self, thread_id):
        self._threads_active[thread_id] = False
