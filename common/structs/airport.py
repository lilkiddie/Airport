from datetime import datetime
from dataclasses import dataclass, field
from common.consts import FlightType, FlightStatus, StatsKey
from collections import deque, namedtuple, defaultdict
from utils.converters import time_to_ticks, ticks_to_time
from random import choices, randint
from common.consts import TIME_TO_LAND, FILEPATH


@dataclass
class Request:
    ticks: int = 0
    flight: 'Flight' = None
    runway_id: int = None
    process_ticks: int = 0


class Experiment:
    FILE_HEADERS = [
        'flight_number',
        'date',
        'status',
        'type'
    ]

    def __init__(self, airport_name: str = 'JFK', n_runways: int = 5, step=1):
        self.flight_board = self.from_csv(filepath=FILEPATH, sep=',')
        self.handler = Handler(n_runways)
        self.name = airport_name
        self.step = step
        self.stats = {key: [0] for key in StatsKey}
        self.ticks = 1130
        self.over = False

        self.get_delays()
        # print(self.flight_board)

    def is_over(self):
        flag = True
        for flight in self.flight_board:
            flag = flag and flight.status != ''
        self.over = flag
        return self.over

    def get_delay_stats(self):
        return dict([self._get_avg_delay(), self._get_max_delay()])

    def _get_avg_delay(self):
        stats = [abs(flight.date_ticks - time_to_ticks(flight.date)) for flight in self.flight_board if flight.status != '']
        delay = 0.0
        if stats:
            delay = sum(stats) / len(stats)

        return (StatsKey.avg_delay, round(delay, 2))

    def _get_max_delay(self):
        value = max([flight.date_ticks - time_to_ticks(flight.date) for flight in self.flight_board if flight.status != ''], default=0)
        return (StatsKey.max_delay, value)

    def get_delays(self):
        for idx in range(len(self.flight_board)):
            flight = self.flight_board[idx]
            p = 0.2
            if flight.type == 'Посадка':
                delay = choices([0, randint(-20, -1), randint(1, 20)], [1 - 2 * p, p, p])[0]
            if flight.type == 'Вылет':
                delay = choices([0, randint(1, 20)], [1 - p, p])[0]
            # print(delay)
            flight.date_ticks += delay

    def __call__(self, force):
        if not force:
            for _ in range(self.step):
                self.process()
        else:
            while not self.over:
                self.process()

    def process(self):
        if self.over:
            return
        for flight in self.flight_board:
            if self.ticks == flight.date_ticks - TIME_TO_LAND:
                request = Request(ticks=self.ticks, flight=flight, process_ticks=TIME_TO_LAND)
                # print(f'sent request {request}')
                self.handler.process(request)
        # for runway in self.handler.runways:
        #     print(runway)
        runways_stats = self.handler(self.ticks)
        for key, value in runways_stats.items():
            self.stats[key].append(value)
        for key, value in self.get_delay_stats().items():
            self.stats[key].append(value)
        self.ticks += 1
        if self.is_over():
            for key, value in self.stats.items():
                match key:
                    case StatsKey.max_delay:
                        self.stats[key] = [max(value)]
                    case StatsKey.avg_delay:
                        self.stats[key] = [self._get_avg_delay()[1]]
                    case StatsKey.max_length:
                        self.stats[key] = [max(value)]
                    case StatsKey.avg_length:
                        self.stats[key] = [round(sum(value) / len(value), 2)]

    def from_csv(self, filepath: str, sep=','):
        with open(filepath) as file:
            headers = tuple(file.readline().strip().split(sep))
            if set(headers) != set(self.FILE_HEADERS):
                raise ValueError('File is invalid')
            RowStruct = namedtuple('RowStruct', self.FILE_HEADERS)
            flight_board = []
            for csv_row in file.readlines():
                row = RowStruct(*csv_row.strip().split(sep))
                flight_board.append(Flight(row.flight_number, row.date, '', FlightType(row.type).value))
            return flight_board

class Handler:
    def __init__(self, n_runways):
        self.runways = [Runway(i) for i in range(n_runways)]

    def __call__(self, ticks):
        for runway in self.runways:
            if len(runway) != 0:
                message = runway.top()
                if message.process_ticks == 0:
                    message = runway.top()
                    runway.pop()
                    message.flight.date_ticks = ticks
                    if message.flight.type == 'Вылет':
                        status = r'Вылетел в {time}'
                    else:
                        status = r'Прилетел в {time}'
                    message.flight.status = status.format(time=ticks_to_time(ticks))
                if len(runway) != 0:
                    message = runway.top()
                    message.process_ticks -= 1
        return dict([self._get_max_queue_length(), self._get_avg_queue_length()])

    def process(self, request: 'Request'):
        runway = self.get_runway()
        runway.append(request)

    def get_runway(self) -> 'Runway':
        return min(self.runways, key=lambda x: len(x))

    def _get_avg_queue_length(self):
        value = 0
        for runway in self.runways:
            value += len(runway)
        return (StatsKey.avg_length, value / len(self.runways) if len(self.runways) else value)

    def _get_max_queue_length(self):
        value = 0
        for runway in self.runways:
            value = max(len(runway), value)
        return (StatsKey.max_length, value)


@dataclass
class Runway:
    id: int
    _queue: deque = field(default_factory=deque)

    def append(self, value):
        self._queue.append(value)
    
    def pop(self):
        self._queue.popleft()
    
    def top(self):
        return self._queue[0]
    
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
    type: str
    date_ticks: int = 0

    def __post_init__(self):
        self.date_ticks = time_to_ticks(self.date)
