from dataclasses import dataclass
from collections import deque
from .airport import RunwayType, FlightStatus


class MessageQueue:
    def __init__(self, maxlen=100):
        self.queue = deque(maxlen=maxlen)

    def __len__(self):
        return len(self.queue)
    
    def get_message(self):
        if self.queue:
            return self.queue.popleft()
        return None
    
    def put_message(self, message):
        self.queue.append(message)


@dataclass(slots=True)
class Request:
    flight_number: str
    type: RunwayType


@dataclass(slots=True)
class Response:
    flight_number: str
    status: FlightStatus
    delay: int = 0
    