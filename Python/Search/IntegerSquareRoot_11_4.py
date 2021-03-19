def square_root(k: int) -> int:

    '''
    :param k: integer
    :return: the closest integer that is less or equal to the squared root of k

    >>> square_root(16)
    4

    >>> square_root(300)
    17

    >>> square_root(63)
    7

    >>> square_root(-1)
    -1

    Brute force: use binary search to find the value. Start from k // 2 -> 0
    if midd * midd == k -> return k
    if midd * midd

    k: 63
    mid = 31, 15, 7, 11, 9, 8
    left: 0, 7, 7
    right: 63, 31, 15, 11, 9, 8

    Time complexity: O(log(n))

    # Try to optimize this code, with just two if conditions...

    '''

    if k < 0:
        return -1

    left, right, result = 0, k, -1

    while left < right:
        mid = left + (right - left) // 2
        if mid * mid == k:
            return mid
        elif mid * mid > k:
            right = mid
        elif mid * mid < k:
            result = mid
            left = mid + 1
    return result


