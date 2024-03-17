from datetime import datetime
from common.structs.airport import FlightType, AircraftType


class Converter:
    def __init__(self, items):
        self._forward = {e[0]: e[1] for e in items}
        self._reverse = {e[1]: e[0] for e in items}

    def _get(self, collection, key):
        value = collection.get(key)
        if value is None:
            raise ValueError
        return value

    def forward(self, key):
        return self._get(self._forward, key)
    
    def reverse(self, key):
        return self._get(self._reverse, key)


aircraft_type_to_ticks = Converter((
    (AircraftType.small, 5),
    (AircraftType.medium, 10),
    (AircraftType.heavy, 30),
))


def total_seconds(time: datetime):
    time = time.time()
    # print(time.hour, time.minute, time.second)
    return ((time.hour * 60) + time.minute) * 60 + time.second
