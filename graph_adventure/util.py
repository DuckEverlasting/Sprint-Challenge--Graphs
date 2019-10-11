class QueueNode:
    def __init__(self, value, next=None, prev=None):
        self.value = value
        self.next = next
        self.prev = prev
  
class Queue:
    def __init__(self):
        self.size = 0
        self.head = None

    def enqueue(self, value):
        newNode = QueueNode(value)
        self.size += 1
        if not self.head:
            self.head = newNode
        else:
            newNode.next = self.head
            self.head.prev = newNode
            self.head = newNode
    
    def dequeue(self):
        if not self.head:
            return None
        self.size -= 1
        if not self.size:
            current_head = self.head
            self.head = None
            return current_head.value
        current_head = self.head
        self.head = self.head.next
        self.head.prev = None
        return current_head.value
        