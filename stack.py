class Stack:
    stack = []
    index = -1

    def __init__(self, url):
        self.stack.append(url)
        self.index = 0

    def add_next(self, other):
        if other not in self.stack:
            print '\t---> ' + other
            self.stack.append(other)

    def has_next(self):
        if self.index < len(self.stack):
            return True
        else:
            return False

    def get_next(self):
        if self.has_next():
            self.index += 1
            print self.stack[self.index-1]
            return self.stack[self.index-1]
        else:
            return None
