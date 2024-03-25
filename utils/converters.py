import datetime


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


def ticks_to_time(ticks):
    h = ticks // 60
    m = ticks % 60
    return datetime.time(h, m).strftime('%H:%M')
