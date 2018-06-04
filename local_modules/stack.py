import threading


class Stack:
    stack = []
    results = []

    def __init__(self, url):
        self.stack.append(url)
        self.index = 0
        self.index_lock = threading.Lock()
        self.append_lock = threading.Lock()
        self.result_lock = threading.Lock()

    def add_next(self, other):
        self.append_lock.acquire()
        if other not in self.stack:
            self.stack.append(other)
        self.append_lock.release()

    def has_next(self):
        if self.index < len(self.stack):
            return True
        else:
            return False

    def get_next(self):
        self.index_lock.acquire()
        if self.has_next():
            url = self.stack[self.index]
            self.index += 1
            self.index_lock.release()
            return url
        else:
            self.index_lock.release()
            return None

    def add_result(self, result):
        self.result_lock.acquire()
        self.results.append(result)
        self.result_lock.release()

    def get_results(self):
        return self.results
