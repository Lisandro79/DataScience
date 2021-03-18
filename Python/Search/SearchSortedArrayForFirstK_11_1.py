from bisect import bisect_left


def find_k(arr: [int], k: int):

    '''
    params: we receive a sorted array and a value k
    bisect_left will return the index to the left of k
    if idx < len(arr), then return idx + 1
    if idx == len(a) return -1

    >>> my_array = [108, 108, 108, 108, 108]
    >>> k = 108
    >>> find_k(my_array, k)
    0

    >>> my_array = [-14, -10, 2, 108, 108, 243, 285, 285, 285, 401]
    >>> k = 108
    >>> find_k(my_array, k)
    3

    >>> my_array = [-14, -10, 2, 108, 108, 243, 285, 285, 285, 401]
    >>> k = 285
    >>> find_k(my_array, k)
    6

    >>> my_array = [-14, -10, 2, 108, 108, 243, 285, 285, 285, 401]
    >>> k = 401
    >>> find_k(my_array, k)
    9

    >>> my_array = [-14, -10, 2, 108, 108, 243, 285, 285, 285, 401]
    >>> k = 501
    >>> find_k(my_array, k)
    -1

    '''


    idx = bisect_left(arr, k)
    if idx < len(arr):
        return idx
    else:
        return -1

def find_k_implement_bisect(arr: [int], k: int):

    '''

    params: we receive a sorted array and a value k
    divide the array in two
    bisect_left will return the index to the left of k
    if idx < len(arr), then return idx + 1
    if idx == len(a) return -1

    >>> my_array = [108, 108, 108, 108, 108]
    >>> k = 108
    >>> find_k(my_array, k)
    0

    >>> my_array = [-14, -10, 2, 108, 108, 243, 285, 285, 285, 401]
    >>> k = 108
    >>> find_k(my_array, k)
    3

    >>> my_array = [-14, -10, 2, 108, 108, 243, 285, 285, 285, 401]
    >>> k = 285
    >>> find_k(my_array, k)
    6

    >>> my_array = [-14, -10, 2, 108, 108, 243, 285, 285, 285, 401]
    >>> k = 401
    >>> find_k(my_array, k)
    9

    >>> my_array = [-14, -10, 2, 108, 108, 243, 285, 285, 285, 401]
    >>> k = 501
    >>> find_k(my_array, k)
    -1
    '''

    # Find middle index
    # Check if k == middle index
    # then we search backwards until we find the first element

    left, right, result = 0, len(arr) - 1, -1
    while left <= right:
        mid_idx = left + (right - left) // 2

        if k > arr[mid_idx]:
            left = mid_idx + 1
        elif k == arr[mid_idx]:
            result = mid_idx
            right = mid_idx - 1

            # final_idx = mid_idx
            # for index in range(mid_idx, 0, -1):
            #     if arr[index] == k:
            #         final_idx = index
            # return final_idx
        else:
            right = mid_idx - 1
    return result


def find_greater_than_key(arr, k):
    '''

        >>> my_array = [108, 108, 108, 108, 108]
        >>> k = 108
        >>> find_greater_than_key(my_array, k)
        -1

        >>> my_array = [-14, -10, 2, 108, 108, 243, 285, 285, 285, 401]
        >>> k = -13
        >>> find_greater_than_key(my_array, k)
        1

        >>> my_array = [-14, -10, 2, 108, 108, 243, 285, 285, 285, 401]
        >>> k = -15
        >>> find_greater_than_key(my_array, k)
        0

        >>> my_array = [-14, -10, 2, 108, 108, 243, 285, 285, 285, 401]
        >>> k = 285
        >>> find_greater_than_key(my_array, k)
        9

        >>> my_array = [-14, -10, 2, 108, 108, 243, 285, 285, 285, 401]
        >>> k = 401
        >>> find_greater_than_key(my_array, k)
        -1

        >>> my_array = [-14, -10, 2, 108, 108, 243, 285, 285, 285, 401]
        >>> k = 501
        >>> find_greater_than_key(my_array, k)
        -1
    '''

    # [-14, -10, 2, 108, 108, 243, 285, 285, 285, 401]

    # left 0,
    # right 9, 3, 0
    # midd_idx 4, 1
    # if k < arr[0] then return 0
    # if k > arr[-1] then return -1
    # else
    # find if k is in the array
    # if k < element N

    if k < arr[0]:
        return 0
    elif k >= arr[-1]:
        return -1

    left, right, result = 0, len(arr) - 1, -1

    while left < right:
        midd_idx = left + (right - left) // 2
        if k < arr[midd_idx]:
            result = midd_idx
            right = midd_idx - 1
        else:
            result = midd_idx + 1
            left = midd_idx + 1

    return result

# my_array = [-14, -10, 2, 108, 108, 243, 285, 285, 285, 401]
# k = 243
# print(find_k(my_array, k))

my_array = [-14, -10, 2, 108, 108, 243, 285, 285, 285, 401]
k = -13
find_greater_than_key(my_array, k)
