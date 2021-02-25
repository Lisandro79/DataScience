class Node:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next


class SLinkedList:
    def __init__(self):
        self.head = None

    # Print the linked list
    def list_print(self) -> object:
        print_val = self.head
        while print_val is not None:
            print(print_val.data)
            print_val = print_val.next

    def at_begining(self, new_data):
        new_node = Node(new_data)

        # Update the new nodes next val to existing node
        new_node.next = self.head
        self.head = new_node


class Functions:

    @staticmethod
    def search_list(list_node, key: int):
        while list_node and list_node.data != key:
            list_node = list_node.next
        # if node is not found it returns null
        return list_node

    @staticmethod
    def insert_after(node, new_node):
        new_node.next = node.next
        node.next = new_node

    @staticmethod
    def delete_after(node):
        node.next = node.next.next
