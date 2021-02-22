import numpy as np

# takes as input an array representing a non-negative integer
# E.g.: <1, 2, 9>
# returns an array representing that integer + 1
# E.g. <1, 3, 0>


# Brute force approach:
# - loop through the array, transform each element into a string and concatenate each char
# - transform the string into an int
# - add 1 to the int
# - convert back to string
# - loop through each char, convert into int and store in an array

# O(2n) time complexity
# O(n)

# Intuition
# sum each element and add pow((0, n), 10) -> 0, 10, 100, 1000 ...


def increment_array_string(arr: list) -> list:
    # O(n) time complexity
    # O(n) space complexity

    arr = arr[::-1]
    decimal = pow(10, np.arange(1, len(arr)))

    integer_sum = 0
    for i in range(len(arr)):
        if i == 0:
            integer_sum += arr[i]
        else:
            integer_sum += arr[i] * decimal[i-1]

    string_sum = str(integer_sum + 1)

    arr_sum = []
    for i in range(len(string_sum)):
        arr_sum.append(int(string_sum[i]))

    return arr_sum


def increment_array_decimal(a: list) -> list:
    # O(n) time complexity
    # O(1) space complexity
    a[-1] += 1  # add 1 to the digit
    for i in reversed(range(1, len(a))):
        if a[i] != 10:
            break
        a[i] = 0
        a[i - 1] += 1
        # else:
        #     remainder = 0
    if a[0] == 10:
        a[0] = 1
        a.append(0)
    return a


A = [9, 9, 9]
print(increment_array_string(A))
print(increment_array_decimal(A))
