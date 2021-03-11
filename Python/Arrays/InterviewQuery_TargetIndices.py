def target_indices(arr, target):
    '''
    >>> target_indices([1, 2, 3, 4], 5)
    [0, 3]
    >>> target_indices([10, 8, 4, 5], 13)
    [1, 3]
    >>> target_indices([9, 8, 4, 5], 13)
    [0, 2]
    >>> target_indices([10, 8, 4, 5], 1398)
    []
    '''

    # O(n) -> loop at most once through the array
    # sort the array
    # use two pointers, one at the beginning and one at the end of the array

    # if arr[left] + right > target -> decrease right
    # if left + right == target -> return left, right indices
    # if left + right < target -> increase left

    sorted_arr = sorted(arr)
    left, right = 0, len(arr) - 1
    while left < right:
        el_sum = sorted_arr[left] + sorted_arr[right]
        if el_sum < target:
            left += 1
        elif el_sum == target:
            return sorted([arr.index(sorted_arr[left]), arr.index(sorted_arr[right])])
        elif el_sum > target:
            right -= 1
    return []


print(target_indices([1, 2, 3, 4], 5))
print(target_indices([10, 8, 4, 5], 13))
