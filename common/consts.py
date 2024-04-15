import enum

__all__ =  [
    'FILEPATH',
    'TIME_TO_LAND',
    'FlightType',
    'FlightStatus',
    'AircraftType',
]


TIME_TO_LAND = 10
FILEPATH = 'test.csv'

class FlightType(enum.Enum):
    landing = 'Посадка'
    take_off = 'Вылет'


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

class StatsKey(enum.Enum):
    avg_delay = 'Среднее отклонение от расписания'
    max_delay = 'Максимальная задержка'
    max_length = 'Максимальная длина очереди'
    avg_length = 'Cредняя длина очереди'
