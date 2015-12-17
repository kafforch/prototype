import time


class TimerService ( ):
    def __init__(self, new_time=0):
        current_time = new_time


__timer_svc = TimerService ( )


def set_time(new_time):
    __timer_svc.current_time = new_time


def get_time():
    return __timer_svc.current_time


def get_current_time():
    return time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
