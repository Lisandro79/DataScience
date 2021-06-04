import functools


def trace(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f'Trace function: {func.__name__}, with args: {args} and kwargs: {kwargs}')

        results = func(*args, **kwargs)

        print(f'Results: {results}')

        return results
    return wrapper


@trace
def my_sum(a, b, factor=0.5):
    return (a + b) * factor


print(my_sum(4, 5, factor=0.2))
print(my_sum.__name__)
