import datetime


def ticks_to_time(ticks):
    h = ticks // 60
    m = ticks % 60
    return datetime.time(h, m).strftime('%H:%M')

def time_to_ticks(time: str):
    time = datetime.datetime.strptime(time, '%H:%M').time()
    return time.hour * 60 + time.minute
