import enum
from datetime import datetime
from functools import cached_property
from dataclasses import dataclass
from .message_queue import Request, Response


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
    is_free: str = None


@dataclass
class Aircraft:
    name: str
    type: AircraftType


@dataclass
class Flight:
    number: str
    departure_date: datetime
    arrival_date: datetime
    status: FlightStatus
    aircraft: Aircraft


@dataclass
class FlightBoard:
    flights: dict[str, Flight]


@dataclass
class ControlRoom:
    flight_board: FlightBoard
    runways: list[Runway]

    @cached_property
    def land_runways(self):
        return [runway for runway in self.runways if runway.type == RunwayType.land]

    @cached_property
    def take_off_runways(self):
        return [runway for runway in self.runways if runway.type == RunwayType.take_off]

    @property
    def landing_delay(self):
        return 15
        
    def __call__(self, request: Request):
        free_runway = self.get_free_runway()
        flight_number, status, delay = request.flight_number, None, 0
        if free_runway is None:
            status = FlightStatus.delayed
            delay = self.landing_delay
        else:
            free_runway.is_free = flight_number
            status = FlightStatus.landing
        response = Response(flight_number, status, delay)

        return response


@dataclass
class Airport:
    name: str
    control_room: ControlRoom
