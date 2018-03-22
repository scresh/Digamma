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

    def elements_left(self):
        return len(self.stack) - self.index + 1

    def add_next(self, other):
        self.append_lock.acquire()
        if other not in self.stack:
            #print '\t---> ' + other
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
            self.index += 1
            self.index_lock.release()
            #print self.stack[self.index - 1]
            return self.stack[self.index - 1]
        else:
            self.index_lock.release()
            return None

    def add_result(self, result):
        self.result_lock.acquire()
        self.results.append(result)
        self.result_lock.release()

    def get_results(self):
        return self.results
