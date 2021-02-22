# get index value
# Force brute approach: search for less, equal, highest than the pivot.
# Fill three vectors with each case, sort each vector and concatenate into one vector again


def arrange_array(arr: list, index: int) -> list:
    # O(n) time complexity
    # O(n) space complexity (because we can overwrite A with the three vectors
    lower = []
    equal = []
    higher = []
    pivot = arr[index]
    for i in arr:
        if i == pivot:
            equal.append(i)
        elif i < pivot:
            lower.append(i)
        else:
            higher.append(i)

    return lower + equal + higher


def arrange_array_opt(arr: list, index: int) -> list:

    # O(n) time complexity
    # O(1) space complexity

    pivot = arr[index]
    smaller, equal, larger = 0, 0, len(arr)

    while equal < larger:
        if arr[equal] < pivot:
            arr[smaller], arr[equal] = arr[equal], arr[smaller]
            smaller += 1
            equal += 1
        elif arr[equal] == pivot:
            equal += 1
        else:
            larger -= 1
            arr[equal], arr[larger] = arr[larger], arr[equal]

    return arr


A = [0, 1, 2, 0, 2, 1, 1]
print(arrange_array(A, 2))
print(arrange_array_opt(A, 2))