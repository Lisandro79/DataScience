
# Why is this a challenge?
# This exercise is trivial if we just take elements of the array and move them into another array
# The purpose of the exercise though, is to show how to perform in place removal and replacement of characters
# The goal is to preserve O(1) space complexity.

# search for the 'b's, remove them
# get the first 4 elements of array
# change the 'a's into 'dd's


def replace_remove(s, size: int) -> [str]:
    # In place removal of characters
    char_to_remove = 'b'
    write_idx, a_count = 0, 0
    for i in range(size):
        if s[i] != char_to_remove:
            s[write_idx] = s[i]
            write_idx += 1
        if s[i] == 'a':
            a_count += 1

    # In place replacement of characters (backwards in this example)
    curr_idx = write_idx - 1
    write_idx += a_count - 1
    while curr_idx >= 0:
        if s[curr_idx] == 'a':
            s[write_idx-1: write_idx + 1] = 'dd'
            write_idx -= 2
        else:
            s[write_idx] = s[curr_idx]
            write_idx -= 1
        curr_idx -= 1

    return s


# Variant of the exercise above:
# Given a string as input, replace chars "." with 'DOT', ',' with  'COMMA',
# '?' with 'QUESTION MARK' and '!' with 'EXCLAMATION MARK'
# The algorithm must have O(1) space complexity

# My approach:
# a- Define a dictionary that maps each char to replace (e.g., '!') to its corresponding string
# b- Make the string a list of chars (to avoid incrementing memory)
# c- Loop through the array replace the chars that match the keys
# d- Joint the elements in the array into a string

# Questions:
# Are steps b and d in the description above O(1) space complexity?

# shift string to the right
# yield index

def telex_encode(sentence: list) -> list:

    """
    # Search for occurrences backwards in the array
    # When a key char is found, we rotate the array to the right until the index is at the end
    # Remove the last character in the sentence
    # Append the new characters to the end -> append has O(1) space complexity this way
    # Rotate the array to the left by n positions to keep the same index
    """

    encodings = dict({".": ['D', 'O', 'T'], ',': ['C', 'O', 'M', 'M', 'A'],
                      '?': ['Q', 'U', 'E', 'S', 'T', 'I', 'O', 'N', ' ', 'M', 'A', 'R', 'K'],
                      '!': ['E', 'X', 'C', 'L', 'A', 'M', 'A', 'T', 'I', 'O', 'N', ' ', 'M', 'A', 'R', 'K']})
    keys = encodings.keys()

    curr_idx = len(sentence) - 1
    while curr_idx >= 0:
        if sentence[curr_idx] in keys:
            key = sentence[curr_idx]
            sentence = sentence[curr_idx+1:] + sentence[:curr_idx+1]  # rotate array to the right
            sentence = sentence[:-1]
            for ch in encodings[key]:
                sentence.append(ch)  # append new chars -> O(1) space complexity

            rot_left = curr_idx + len(encodings[key])  # rotate array to the left
            sentence = sentence[-rot_left:] + sentence[:-rot_left]

        curr_idx -= 1

    return sentence


a = ['a', 'c', 'd', 'b', 'b', 'c', 'a']
print(replace_remove(a, size=7))

a = ['I', 't', 'i', 's', 'a', '(', '!', ')', 'n', 'o', '?']
print(telex_encode(a))

