class Link:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

    def __str__(self):
        if not self.next:
            return f"Link({self.val})"
        return f"Link({self.val}, {self.next})"


def merge_k_linked_lists(linked_lists):
    '''
    Merge k sorted linked lists into one
    sorted linked list.
    >>> print(merge_k_linked_lists([
    ...     Link(1, Link(2)),
    ...     Link(3, Link(4))
    ... ]))
    Link(1, Link(2, Link(3, Link(4))))
    >>> print(merge_k_linked_lists([
    ...     Link(1, Link(2)),
    ...     Link(2, Link(4)),
    ...     Link(3, Link(3)),
    ... ]))
    Link(1, Link(2, Link(2, Link(3, Link(3, Link(4))))))
    '''

    '''
    Input: sorted linked lists
    Brute force approach: store all the values for each node in the linked lists into an array
    Then construct a new LinkedList adding those nodes to the list.
        
    '''
    node_values = []
    for link in linked_lists:
        while link:
            node_values.append(link.val)
            link = link.next
    node_values.sort()

    result = Link(0)
    pointer = result
    for val in node_values:
        pointer.next = Link(val)
        pointer = pointer.next
    return result.next


linked_lists = [Link(1, Link(2, Link(8))), Link(4, Link(6, Link(7)))]
merge_k_linked_lists(linked_lists)
# print(link)
for id, llist in enumerate(linked_lists):
    print(f"List id : {id}")
    while llist:
        print(llist.val)
        llist = llist.next
