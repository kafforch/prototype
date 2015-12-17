from datetime import datetime

TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.000Z"
INPUT_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

class TimerService:
    def __init__(self, new_time=0):
        self.current_time = new_time


__timer_svc = TimerService()


def set_datetime(new_time):
    if isinstance(new_time, basestring):
        __timer_svc.current_time = datetime.strptime(new_time, INPUT_TIME_FORMAT)
    else:
        __timer_svc.current_time = new_time


def get_datetime():
    return __timer_svc.current_time


def get_datetime_str():
    return datetime.strftime( get_datetime(), TIME_FORMAT )


def get_current_datetime():
    return datetime.utcnow()


def get_current_datetime_str():
    return datetime.strptime(get_current_datetime(), TIME_FORMAT)


def is_current_datetime_later_than(time_in_str):
    time_in = time_in_str
    if isinstance(time_in_str, basestring):
        time_in = datetime.strptime(time_in_str, INPUT_TIME_FORMAT)

    return time_in < get_datetime()
