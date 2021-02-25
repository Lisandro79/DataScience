# Get all values of each linkedList and store them in an array. Sort values
# Loop through the array and check, for each linkedList if the value coincides with the current node
# Create a new list

from Python.LinkedLists.API.API import Node, SLinkedList


def merge_sorted_lists(list1: [Node], list2: [Node]):

    # Search until both lists reach the end
    head = tail = Node()
    while list1 and list2:
        if list1.data < list2.data:
            tail.next = list1
            list1 = list1.head.next
        else:
            tail.next = list2
            list2 = list2.head.next

    return head.next

# L1 = SLinkedList()
# L1.head = Node(2)
# e2 = Node(5)
# e3 = Node(7)
# L1.head.next = e2
# e2.next = e3
# L1.list_print()
L1 = [Node(2), Node(5), Node(7)]


# L2 = SLinkedList()
# L2.head = Node(3)
# e2 = Node(11)
# L2.head.next = e2
# L2.list_print()
L2 = [Node(3), Node(11)]

merge_sorted_lists(L1, L2)
