
# Compute parity (odd / even) or a 64 bit word
# brute force approach: iterate through each binary digit and count
# use modulo to determine odd / even

# more efficient: use two pointers and reduce iteration time by 2


def compute_parity(x: int):

    n_bits = 0
    while x:
        n_bits ^= 1 & x
        x >>= 1

    return n_bits


print("0: {}".format(compute_parity(0)))
print("1: {}".format(compute_parity(1)))
print("3: {}".format(compute_parity(3)))
print("8: {}".format(compute_parity(8)))