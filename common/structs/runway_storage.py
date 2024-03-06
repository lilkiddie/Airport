from dataclasses import dataclass


@dataclass
class Node:
    value: int = 0
    next: 'Node' = None
    prev: 'Node' = None


class Storage:
    def __init__(self, n_runways=10):
        head, tail = Node(-1), Node(-1)
        head.next, tail.prev = tail, head
        self.head, self.tail = head, tail
        self.storage = dict()

        for id in range(1, n_runways):
            pass

    def _insert(self, value):
        node = Node(value, self.head.next, self.head)
        self.head.next.prev = node
        self.head.next = node
