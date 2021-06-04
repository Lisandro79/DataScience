import functools
import time


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(**kwargs)
        print(result)
        total_time = time.time() - t1
        return total_time
    return wrapper


@timer
def mock_time_interval(sleep_interval=0.4):
    time.sleep(sleep_interval)
    return 'Patience is the mother of who?'


total_time = mock_time_interval(sleep_interval=0.8)
print(total_time)
