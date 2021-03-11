# @author Liam Pulsifer
# Tiny little timing function
# Usage:
# @timed_func
# def my_func():
#   return 5

import time
def timed_func(func_to_time):
    def timed(*args, **kwargs):
        start = time.perf_counter()
        res = func_to_time(*args, **kwargs)
        print(time.perf_counter() - start)
        return res
    return timed
