from collections import deque

class Stack():
    def __init__(self):
        self.stack = deque()

    def add(self, value):
        self.stack.append(value)

    def get(self):
        return self.stack.pop()

    def getList(self):
        lst1 = list()
        for i in range(len(self.stack)):
            lst1.append(self.stack.pop())
        lst2 = lst1[::-1]
        return lst2

    def __len__(self):
        return len(self.stack)

