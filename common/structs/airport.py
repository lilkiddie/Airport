import enum
from datetime import datetime
from dataclasses import dataclass


class RunwayType(enum.Enum):
    land = 1
    take_off = 2


class FlightStatus(enum.Enum):
    landing = 1
    landed = 2
    delayed = 3


class AircraftType(enum.Enum):
    small = 'small'
    medium = 'medium'
    heavy = 'heavy'


@dataclass
class Runway:
    id: int
    type: RunwayType


@dataclass
class Aircraft:
    name: str
    type: AircraftType

    def send_request(message, queue):
        queue.push(message)


@dataclass
class Flight:
    number: str
    departure_date: datetime
    arrival_date: datetime
    status: FlightStatus
    aircraft: Aircraft


@dataclass
class FlightBoard:
    flights: list[Flight]

    @classmethod
    def read_csv(cls, file_path, sep=','):
        with open(file_path) as file:
            _ = file.readline()
            return cls(
                flights=[Flight(*line) for line in file.readlines()]
            )


@dataclass
class ControlRoom:
    flight_board: FlightBoard
    runways: list[Runway]

    def process_request():
        pass


@dataclass
class Airport:
    name: str
    control_room: ControlRoom
