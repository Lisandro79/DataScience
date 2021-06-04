# @author Liam Pulsifer
#
# A basic insertion sort, modified slightly to allow sorting
# a slice of a list rather than the full list if desired.
# O(n^2) in worst case.
def insertion_sort(items, left=0, right=None):
    if right is None: # If None, we want to sort the full list
        right = len(items) - 1
    for i in range(left + 1, right + 1): # If right is len(items) - 1, this sorts the full list.
        current_item = items[i]
        j = i - 1 # Chose the element right before the current element

        while (j >= left and current_item < items[j]): # Break when the current el is in the right place
            items[j + 1] = items[j] # Moving this item up 
            j -= 1 # Traversing "leftwards" along the list
        
        items[j + 1] = current_item # Insert current_item into its correct spot

    return items