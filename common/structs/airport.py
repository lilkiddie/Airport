from datetime import datetime
from dataclasses import dataclass, field
from common.consts import FlightType, FlightStatus
from build.ui import GUI
from collections import deque, namedtuple




@dataclass
class Request:
    ticks: int = 0
    flight: 'Flight' = None
    runway_id: int = None


class Experiment:
    FILE_HEADERS = [
        'flight_number',
        'date',
        'status',
        'type'
    ]

    def __init__(self, filepath: str, airport_name: str = 'Test', n_runways: int = 5):
        self.flight_board = self.from_csv(filepath=filepath, sep=',')
        self.handler = Handler(n_runways)
        self.name = airport_name
        self.requests = []
        self._history = []
        self.ticks = 0

    def __call__(self):
        for flight in self.flight_board:
            if self.ticks == flight.date_ticks:
                request = Request(ticks=self.ticks, flight=flight)
                print(f'sent request {request}')
                self.handler.process(Request(ticks=self.ticks, flight=flight))
        for runway in self.handler.runways:
            print(runway)
        self.handler(self.ticks)
        self.ticks += 1
    
    def from_csv(self, filepath: str, sep=','):
        with open(filepath) as file:
            headers = tuple(file.readline().strip().split(sep))
            if set(headers) != set(self.FILE_HEADERS):
                raise ValueError('File is invalid')
            RowStruct = namedtuple('RowStruct', self.FILE_HEADERS)
            flight_board = []
            for csv_row in file.readlines():
                row = RowStruct(*csv_row.strip().split(sep))
                flight_board.append(Flight(row.flight_number, row.date, row.status, row.type))
            return flight_board


class Handler:
    def __init__(self, n_runways):
        self.runways = [Runway(i) for i in range(n_runways)]

    def __call__(self, ticks):
        stats = []
        for runway in self.runways:
            if len(runway) != 0:
                message = runway.pop()
                message.flight.date_ticks = ticks
                stats.append(message)
        return stats

    def process(self, request: 'Request'):
        runway = self.get_runway()
        runway.append(request)

    def get_runway(self) -> 'Runway':
        return min(self.runways, key=lambda x: len(x))


@dataclass
class Runway:
    id: int
    _queue: deque = field(default_factory=deque)

    def append(self, value):
        self._queue.append(value)
    
    def pop(self):
        return self._queue.popleft()
    
    def __len__(self):
        return len(self._queue)

    def __call__(self):
        pass


@dataclass
class FlightBoard:
    flights: dict[str, 'Flight']

    def get(self, key, default=None):
        return self.flights.get(key, default)

    def __call__(self):
        pass


@dataclass
class Flight:
    number: str
    date: datetime
    status: FlightStatus
    type: FlightType
    date_ticks: int = 0

    def change(self):
        self.number = "ABA"