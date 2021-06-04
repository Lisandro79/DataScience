import time
from contextlib import contextmanager

'''
Dave Brondsema gave a great talk on Decorators and Context Managers at PyCon 2012. 
He mentioned hat we should use context managers when we see any of the following 
patterns in our code:

Open - Close 
Lock - Release
Change - Reset
Enter - Exit (see example below)
Start - Stop
'''


@contextmanager
def execution_time_with_context():
    try:
        initial_time = time.time()
        yield initial_time
    finally:
        total_time = time.time() - initial_time
        print(f'It took: {total_time}')
        # Resource is released at the end of this block,
        # even if code in the block raises an exception


class ExecutionTimer:
    def __init__(self):
        self.total_time = 0
        self.initial_time = 0

    def __enter__(self):
        self.initial_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.total_time = time.time() - self.initial_time
        print(f'It took: {self.total_time}')

    def tell_joke(self, text):
        print(f'{text}  {self.total_time}')


if __name__ == '__main__':

    with execution_time_with_context() as et:
        time.sleep(1)

    with ExecutionTimer() as et:
        et.tell_joke("Gummy bear")
        time.sleep(0.4)
