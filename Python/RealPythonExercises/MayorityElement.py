from collections import Counter
import numpy as np


def majority_element_indexes(lst):
    '''
    Return a list of the indexes of the majority element.
    Majority element is the element that appears more than
    floor(n / 2) times.
    If there is no majority element, return []
    >>> majority_element_indexes([1, 1, 2])
    [0, 1]
    >>> majority_element_indexes([1, 2])
    []
    >>> majority_element_indexes([])
    []
    '''

    # Get the threshold
    n = len(lst)
    # Find the majority element
    count = Counter(lst)
    indexes = []
    # find the indexes
    for key in count.keys():
        if count[key] > np.floor(n / 2):
            for idx, value in enumerate(lst):
                if value == key:
                    indexes.append(idx)
            return indexes
    return []


print(majority_element_indexes([1, 9, 9]))

