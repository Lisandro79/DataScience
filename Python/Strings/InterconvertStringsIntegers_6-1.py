
# store string as a list?
# make a lookup table for numbers as strings
# loop through the string

#
# def string_to_integer(digits: string) -> int:
#     numeric = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
#     sign = '-'
#     isNeg = False
#     integer = []
#
#     for idx in range(0, digits):
#         # Check sign
#         if digits[0] == sign:
#             isNeg = True
#             continue
#
#         # Convert string to integer
#         integer.append(idx)
#
#     return integer *
#
#
# string_to_integer('123')
# string_to_integer('-321')

import functools
import string


def integer_to_string(x: int) -> str:
    is_neg = False
    if x < 0:
        is_neg, x = True, -x

    s = []
    while True:
        s.append(chr(ord('0') + x % 10))
        x //= 10
        if x == 0:
            break

    return ('-' if is_neg else '') + ''.join(reversed(s))


def string_to_integer(s):
    return functools.reduce(
        lambda running_sum, c: running_sum * 10 + string.digits.index(c),
        s[s[0] == '-':], 0) * (-1 if s[0] == '-' else 1)


print(integer_to_string(-8731))
print(string_to_integer('732'))
