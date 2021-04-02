# Get all values of each linkedList and store them in an array. Sort values
# Loop through the array and check, for each linkedList if the value coincides with the current node
# Create a new list

from API import Node, LList


class Node:
    def __init__(self, data=0, next=None):
        self.data = data
        self.next = next


def merge_sorted_lists(list1, list2):
    '''
    :param list1: sorted linked list
    :param list2: sorted linked list
    :return: a merged sorted linked list

    '''

    values = []
    lists = [list1, list2]
    for _, linked_list in enumerate(lists):
        lst = linked_list.head
        while lst:
            values.append(lst.data)
            lst = lst.next
            
    values.sort()

    # Search until both lists reach the end
    sorted_list = LList()
    pointer = Node(values[0])
    sorted_list.head = pointer
    for val in enumerate(values, start=1):
        pointer.next = Node(val)  # link current node to the next one
        pointer = pointer.next  # override current node

    return sorted_list.list_print()


L1 = Node(0)
e1 = Node(2)
e2 = Node(5)
e3 = Node(7)

L1.head = e1
e1.next = e2
e2.next = e3
# L1.list_print()
# L1 = [Node(2), Node(5), Node(7)]


L2 = LList()
e1 = Node(3)
e2 = Node(6)
e3 = Node(90)

L2.head = e1
e1.next = e2
e2.next = e3
# L2.list_print()

# l2 = L2.head
# print(l2.data)

# e1 = Node(3)
# e2 = Node(11)
# e1.next = e2
#
merge_sorted_lists(L1, L2)
