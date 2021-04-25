def find_three_largest_numbers(array):
    '''
    :param array: unsorted array of integers (at least 3 elements)
    :return: three largest values in sorted order
    >>> find_three_largest_numbers([141, 1, 17, -7, -17, -27, 18, 541, 8, 7, 7])
    [18, 141, 541]
    '''

    three_largest_array = [None, None, None]
    for num in array:
        update_largest(three_largest_array, num)
    return three_largest_array


def update_largest(three_largest_array, num):
    if three_largest_array[2] is None or num > three_largest_array[2]:
        shift_update(three_largest_array, num, 2)
    elif three_largest_array[1] is None or num > three_largest_array[1]:
        shift_update(three_largest_array, num, 1)
    elif three_largest_array[0] is None or num > three_largest_array[0]:
        shift_update(three_largest_array, num, 0)


def shift_update(array, num, idx):
    for i in range(idx + 1):
        if i == idx:
            array[i] = num
        else:
            array[i] = array[i + 1]
