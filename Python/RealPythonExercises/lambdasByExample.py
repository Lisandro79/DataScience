import numpy as np

# Use lambdas in the key of Sort
cmp = ['Lisandro Kaunitz', 'Juan Kaunitz', 'Lorenzo Pelle', 'Ignacio Barcelona', 'katia Giacomozzi']
cmp.sort(key=lambda x: x.split()[-1].upper(), reverse=False)
print(cmp)

# Sorting a list of tuples
lst = [('Juan', 3), ('Lisandro', 4), ('Ignacio', 10), ('Katia', -3)]
lst.sort(key=lambda x: x[0], reverse=False)
print(lst)


# Sorting list of objects
class Person:
    def __init__(self, name, age):
        self.age = age
        self.name = name

    def __repr__(self):
        return f"Person({self.name}, {self.age})"


juan = Person('Juan', 38)
lisandro = Person('Lisandro', 41)
cesar = Person('Cesar', 39)
people = [juan, lisandro, cesar]
print(people)
people.sort(key=lambda x: x.age, reverse=True)
print(people)

# Lambdas with Filter()
# filter(function, iterable)
nums = range(1, 21)
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)

nums = [1, 2, 4, 5, 6, 7, 8, 9]
print(f"Mean of nums: {np.mean(nums)}")
above_mean = list(filter(lambda x: x > np.mean(nums), nums))
print(above_mean)


# Lambdas with Map()
# map(function, iterable) -> returns another iterable
nums = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 3, nums))
print(squared)

nums = range(1, 11)
even = list(map(lambda x: x % 2 == 0, nums))
print(even)

people = [('Juan', 3), ('Lisandro', 4), ('Ignacio', 10), ('Katia', -3)]
squared = list(map(lambda person: (person[0], person[1] ** 2), people))
print(squared)


# Lambdas with Reduce
# Reduce(function, iterable)
# Applies the function cumulatively to each element of the iterable

from functools import reduce
nums = [1, 2, 36, 4, 5]
total = reduce(lambda x, y: x + y, nums)
print(f"Total sum: {total}")

maxima = reduce(lambda x, y: x if x > y else y, nums)
print(f"Maximum: {maxima}")

cmp = ['Lisandro Kaunitz', 'Juan Kaunitz', 'Lorenzo Pelle', 'Ignacio Barcelona', 'katia Giacomozzi']
concat = reduce(lambda x, y: x + y[:2], cmp, '')  # second optional parameter represente the 1st element in the list
print(concat)


# Testing Lambda functions
import unittest
squared = lambda x: x ** 2


class LambdaTest(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(squared(3), 9)

    def test_zero(self):
        self.assertEqual(squared(0), 0)

    def test_negative(self):
        self.assertEqual(squared(-5), 25)


if __name__ == 'main':
    unittest.main()
