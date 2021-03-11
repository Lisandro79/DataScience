keypad = {'2': ['a', 'b', 'c'],
          '3': ['d', 'e', 'f'],
          '4': ['g', 'h', 'i'],
          '5': ['j', 'k', 'l'],
          '6': ['m', 'n', 'o'],
          '7': ['p', 'q', 'r', 's'],
          '8': ['t', 'u', 'v'],
          '9': ['w', 'x', 'y', 'z'],
          '0': [' ']}


def keypad_string(keys):
    '''
    Given a string consisting of 0-9,
    find the string that is created using
    a standard phone keypad
    | 1        | 2 (abc) | 3 (def)  |
    | 4 (ghi)  | 5 (jkl) | 6 (mno)  |
    | 7 (pqrs) | 8 (tuv) | 9 (wxyz) |
    |     *    | 0 ( )   |     #    |
    You can ignore 1, and 0 corresponds to space
    >>> keypad_string("12345")
    'adgj'
    >>> keypad_string("4433555555666")
    'hello'
    >>> keypad_string("2022")
    'a b'
    >>> keypad_string("")
    ''
    >>> keypad_string("111")
    ''
    '''

    if not keys:
        return ''

    previous_key = None
    dial_pointer = 0
    word = []
    for idx, key in enumerate(keys, start=1):

        if key == '1':
            pass

        elif previous_key is None:
            previous_key = key
            continue

        elif key == previous_key:  # repeated number
            if dial_pointer >= len(keypad[previous_key]) - 1:  # end of pad
                word.append(keypad[previous_key][dial_pointer])
                previous_key = key
                dial_pointer = 0
            else:
                dial_pointer += 1
                if idx == len(keys):
                    word.append(keypad[previous_key][dial_pointer])
                    break
        else:
            word.append(keypad[previous_key][dial_pointer])
            dial_pointer = 0  # new number
            previous_key = key
            if idx == len(keys):
                word.append(keypad[previous_key][dial_pointer])

    return "".join(word)


# Create a dictionary with key = number and content the letters
# Check the last press, if repeated, keep moving within key.

# Check if we've reached the end of the pad. If so, save the char and restart the pointer

# if number is new, save the last char and start counting the next string

# if we reach the end of the string, we need to add the final number


print(keypad_string("4433555555666"))
