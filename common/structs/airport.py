from datetime import datetime
from dataclasses import dataclass, field
from common.consts import FlightType, FlightStatus, AircraftType
from utils.converters import aircraft_type_to_ticks
from random import choices, randint
from .queue import Queue
import pprint


class Airport:
    def __init__(self, name: str, flight_board: 'FlightBoard', aircrafts: list['Aircraft'], n_runways: int):
        self.name = name
        self.flight_board = flight_board
        self.aircrafts = aircrafts
        self.handler = Handler(n_runways)
        self._ticks = 0

    def __call__(self):
        print(f'{self.__class__.__name__} ticks')
        for aircraft in self.aircrafts:
            aircraft(self.handler, self.flight_board.get(aircraft.flight_number))
        self.handler()
        self._ticks += 1
        pprint.pprint(self.flight_board.flights)
        print()
            

@dataclass
class Aircraft:
    name: str
    flight_number: int
    type: AircraftType
    status: FlightStatus = FlightStatus.ok
    process_ticks: int = 0
    queue_id: int = -1
    _ticks: int = 0
    _probs = [0.8, 0.1, 0.1]

    def __call__(self, handler: 'Handler', flight: 'Flight'):
        print(f'{self.__class__.__name__} {self.flight_number} ticks')
        if self.status == FlightStatus.done:
            flight.date_ticks = self._ticks
            return
        flight.date_ticks += choices([0, randint(-10, -1), randint(1, 10)], self._probs)[0]
        handler.process(self, flight)
        flight.status = self.status
        self._ticks += 1
        pprint.pprint(self)
        print()


class Handler:
    def __init__(self, n_runways):
        self.runways = [Runway(i) for i in range(n_runways + 1)]
    
    def __call__(self):
        print(f'{self.__class__.__name__} ticks')
        for idx, runway in enumerate(self.runways):
            if idx == 0:
                continue
            runway()
    
    def process(self, message: 'Aircraft', flight: 'Flight'):
        if message.status == FlightStatus.done:
            return
        if message.status == FlightStatus.processing:
            if message.process_ticks == aircraft_type_to_ticks.forward(message.type):
                message.status = FlightStatus.done
                flight.date_ticks = message._ticks
            message.process_ticks += 1
        if message.queue_id == -1 and flight.date_ticks - message._ticks - aircraft_type_to_ticks.forward(message.type) <= 0:
            runway = self.get_runway()
            message.queue_id = runway.id
            message.status = FlightStatus.queued
            runway.queue.append(message)
        runway = self.runways[message.queue_id]
        if len(runway.queue) and runway.queue.top() == message and message.status == FlightStatus.queued:
            message.status = FlightStatus.processing
            message.process_ticks = 1

    def get_runway(self) -> Queue:
        runway = None
        ticks = float('inf')
        for idx, e in enumerate(self.runways):
            if idx == 0:
                continue
            if e.queue.ticks < ticks:
                ticks = e.queue.ticks
                runway = e
        print(f'Runway {runway.id} selected')
        return runway


@dataclass
class Runway:
    id: int
    queue: Queue = field(default_factory=Queue)

    def __call__(self):
        print(f'{self.__class__.__name__} {self.id} ticks')
        if not self.queue.queue:
            return
        value = self.queue.top()
        if value.status == FlightStatus.done:
            self.queue.pop()
        
        pprint.pprint(self.queue.queue)
        print(self.queue.ticks)
        print()


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
    date_ticks: int
