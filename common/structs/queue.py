from collections import deque
from dataclasses import dataclass
from utils.converters import aircraft_type_to_ticks


class Queue:
    def __init__(self, maxlen=100):
        self.queue = deque(maxlen=maxlen)

    def __len__(self):
        return len(self.queue)

    def append(self, value):
        self.queue.append(value)
    
    def pop(self):
        value = self.queue.popleft()
        return value
    
    def top(self):
        return self.queue[0]
