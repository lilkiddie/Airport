import enum

__all__ =  [
    'FlightType',
    'FlightStatus',
    'AircraftType',
]


class FlightType(enum.Enum):
    landing = 1
    take_off = 2

    @classmethod
    def from_str(cls, value):
        match(value):
            case 'landing':
                return cls.landing
            case 'take off':
                return cls.take_off
        return None


class FlightStatus(enum.Enum):
    ok = 1
    processing = 2
    delayed = 3
    done = 4
    queued = 5


class AircraftType(enum.Enum):
    small = 'small'
    medium = 'medium'
    heavy = 'heavy'
