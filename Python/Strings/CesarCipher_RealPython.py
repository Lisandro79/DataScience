import string

# ord()
# char()

# all solutions here:
# https://realpython.com/python-practice-problems/#python-practice-problem-1-sum-of-a-range-of-integers
# Solution using built-ins translate(), maketrans()
def caesar(plain_text, shift_num=1):
    letters = string.ascii_lowercase
    mask = letters[shift_num:] + letters[:shift_num]
    trantab = str.maketrans(letters, mask)
    return plain_text.translate(trantab)


# My solution
def cesar_cipher(message, shift):
    '''
    :param message: chars to "shift"
    :param shift: amount of shift to the right
    :return: shifted message
    >>> cesar_cipher('abcd xyz', 4)
    'efgh bcd'
    >>> cesar_cipher('efgh', 1)
    'fghi'
    '''

    # loop through the message and 'shift' letters one by one using modulus operator
    alphabet = string.ascii_lowercase
    result = ''
    for character in message:

        if character not in alphabet:
            result += character
        else:
            # find index of the char in the letters array
            idx = alphabet.index(character) + shift  # shift to the right

            # select the char that is 'shifted' n positions to the right
            shifted_idx = idx % len(alphabet)
            result += alphabet[shifted_idx]

    return result
