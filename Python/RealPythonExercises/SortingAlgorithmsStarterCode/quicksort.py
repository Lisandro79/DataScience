# @author Liam Pulsifer
# A very basic, non-optimized version of Quicksort.
# In-place, but not stable.

import random

def quicksort(items):
    if (len(items) <= 1):
        return items
    pivot = random.choice(items)
    less_than_pivot = [x for x in items if x < pivot]
    equal_to_pivot = [x for x in items if x == pivot]
    greater_than_pivot = [x for x in items if x > pivot]

    # Recursively divide the list into elements greater than, less than,
    # and equal to a chose pivot, then combine the lists as below using recursion.
    return quicksort(less_than_pivot) + equal_to_pivot + quicksort(greater_than_pivot)