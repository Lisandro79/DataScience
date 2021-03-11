import random
import time


def square(num):
    '''
    Let's square some numbers
    >>> square(5)
    25
    >>> square(10)
    100
    '''
    return num * num


def triple(num):
    while True:
        yield 3 * num
        num = 3 * num


# Dictionaries (ordered as created from python 3.7)
bad_guys = dict()
bad_guys['batman'] = 'joker'
bad_guys = {'superman': 'lex lutor', 'batman': 'joker', 'he-man': 'moonra'}
bad_guys['wonderwoman'] = 'jane'

del bad_guys['superman']
bad_guys.pop('wonderwoman')  # return value
# bad_guys.popitem('batman')  # returns tuple

bad_guys2 = {'superman': 'lex lutor', 'batman': 'joker', 'he-man': 'moonra'}
bad_guys2.update(batman='faggot')

bad_guys.update(bad_guys2)

lst = list(bad_guys.items())  # extract dictionary elements to list
list(bad_guys.keys())
list(bad_guys.values())

'batman' in bad_guys  # check existence of key
bad_guys.get('batman ')

# Sort Dictionaries
animals = [{'type': 'cat', 'name': 'Stephanie', 'age': 8},
           {'type': 'dog', 'name': 'Devon', 'age': 3},
           {'type': 'rhino', 'name': 'Moe', 'age': 5}]

print(sorted(animals, key=lambda animal: animal['type'], reverse=True))

# List comprehensions: square a list of numbers
lst = [1, 2, 4, 5, 6]
squared_list = [square(num) for num in lst]
print(f"Square with list Comprehension {squared_list}")
print(f"Square with Map: {list(map(square, lst))}")

squared_lambda = [(lambda x: x * x)(num) for num in lst if num > 1]
print(f"Squared with lambda {squared_lambda}")

# Defaultdict


# lambdas


# Set: operate in O(n) for searching and adding elements. Useful to search for elements and remove duplicates
# Sets store elements in a manner that allows near-constant-time checks whether a value is in the set or not,
# unlike lists, which require linear-time lookups
# {}
all_words = 'hello world how is this world today how'.split()
words = set()
for _ in range(10):
    word = random.choice(all_words)
    words.add(word)

print(f"These are the unique words {words}")


# Generators: https://realpython.com/introduction-to-python-generators/
# useful when we need to process data without increasing memory
# Generator expressions are perfect for when you know you want to retrieve data from a sequence,
# but you don’t need to access all of it at the same time.
# The design allows generators to be used on massive sequences of data,
# because only one element exists in memory at a time.
# square of numbers
tic = time.perf_counter()
n = 10000000
cubes = sum([pow(i, 3) for i in range(0, n)])
print(f"Cubes with list comprehension, {n} elements, time {time.perf_counter() - tic}")
tic = time.perf_counter()
cubes = (pow(i, 3) for i in range(0, n))
print(f"Cubes with a generator, {n} elements, time {time.perf_counter() - tic}")
print(next(cubes), next(cubes), next(cubes))

trip = triple(5)
print(next(trip), next(trip), next(trip))

# Collections.deque: allows insertion and pop with O(1) time complexity


# Namedtuple: fast and simple way to create an immutable class and object


# String module: useful to compare string constants (using sets)
# ord() -> char to num
# char() -> num to char
# translate(), maketrans()
# string.ascii_lowercase, uppercase, letters


# functools reduce -> combine elements of a list into some value


# itertools


# Doctests and assert
# assert <condition>, error
x = 10
assert x >= 0, "X must be positive"



