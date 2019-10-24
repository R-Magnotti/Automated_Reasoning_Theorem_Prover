#**********************************************************************************************************************
#CSC 442: Artificial Intelligence
#Data structures used in tree conversion
#Author: Rich Magnotti (netid: rmagnott@ur.rochester.edu)
#**********************************************************************************************************************

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

#abstract data structure classes
class ExpTree:
    def __init__(self, tok):
        self.token = tok
        self.leftChild = None
        self.rightChild = None

class Stack: #isEmpty, push, pop
    def __init__(self):
        self.items = []

    def isEmpty(self):
        # returns T or F
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def peek(self):
        return self.items[-1]

    def pop(self):
        return self.items.pop()

    def printS(self):
        for item in self.items:
            print(item)