from collections import deque


class MesageQueue:
    def __init__(self, maxlen=100):
        self.queue = deque(maxlen=maxlen)
    
    def get_message(self):
        if self.queue:
            return self.queue.popleft()
        return None
    
    def put_message(self, message):
        self.queue.append(message)
