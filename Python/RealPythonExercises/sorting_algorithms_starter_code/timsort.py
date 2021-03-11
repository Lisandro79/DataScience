# @author Liam Pulsifer
# A simplified TimSort (check out the real code if you're
# looking for a code analysis project).
# Uses both insertion- and merge-sort strategies to produce a 
# stable, fast sort that uses existing runs in the data.

from insertion_sort import insertion_sort
from merge_sort import merge_sorted_lists

def timsort(items):
    min_subsection_size = 32

    # Sort each subsection of size 32
    # (The real algorithm carefully chooses a subsection size for performance.)
    for i in range(0, len(items), min_subsection_size):
        insertion_sort(items, i, min((i + min_subsection_size - 1), len(items) - 1))

    # Move through the list of subsections and merge them using merge_sorted_lists
    # (Again, the real algorithm carefully chooses when to do this.)
    size = min_subsection_size
    while size < len(items):    
        for start in range(0, len(items), size * 2):
            midpoint = start + size - 1
            end = min((start + size * 2 - 1), (len(items) - 1)) # arithmetic to properly index

            # Merge using merge_sorted_lists
            merged_array = merge_sorted_lists(
                items[start:midpoint + 1], 
                items[midpoint + 1:end + 1])
            
            items[start:start + len(merged_array)] = merged_array # Insert merged array
        size *= 2 # Double the size of the merged chunks each time until it reaches the whole list
    
    return items