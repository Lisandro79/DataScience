# @author Liam Pulsifer
# A basic merge sort implementation.
# O(n log(n)) performance.

def merge_sorted_lists(left, right):
    left_index, right_index = 0, 0 # Start at the beginning of both lists
    return_list = []
    while (len(return_list) < len(left) + len(right)):

        # Choose the left-most item from each list that has yet to be processed
        # If all are processed, choose an "infinite" value so we know to not consider that list.
        left_item = left[left_index] if left_index < len(left) else float('inf')
        right_item = right[right_index] if right_index < len(right) else float('inf')
        if (left_item < right_item): # Choose the smallest remaining item
            return_list.append(left_item)
            left_index += 1 # And move up in the list so we don't consider it again
        else:
            return_list.append(right_item)
            right_index += 1
    return return_list

# The actual merge sort is super simple!
def merge_sort(items):
    if (len(items) <= 1):
        return items
    midpoint = len(items) // 2
    left, right = items[:midpoint], items[midpoint:]

    # Recursively divide the list into 2, sort it, and then merge those lists
    return merge_sorted_lists(merge_sort(left), merge_sort(right))