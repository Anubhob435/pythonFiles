class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeTwoLists(l1, l2):
    """
    Merge two sorted linked lists into a single sorted linked list.
    
    Args:
        l1: The head of the first sorted linked list
        l2: The head of the second sorted linked list
        
    Returns:
        The head of the merged sorted linked list
    """
    # Create a dummy head to simplify edge cases
    dummy = ListNode(-1)
    current = dummy
    
    # Traverse both lists and compare values
    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next
    
    # Attach remaining nodes from either list
    if l1:
        current.next = l1
    else:
        current.next = l2
    
    return dummy.next

# Example usage
def create_linked_list(values):
    """Helper function to create a linked list from a list of values"""
    dummy = ListNode(0)
    current = dummy
    for val in values:
        current.next = ListNode(val)
        current = current.next
    return dummy.next

def print_linked_list(head):
    """Helper function to print a linked list"""
    values = []
    current = head
    while current:
        values.append(str(current.val))
        current = current.next
    return " -> ".join(values)

# Test with example lists
list1 = create_linked_list([1, 2, 4])
list2 = create_linked_list([1, 3, 4])
merged = mergeTwoLists(list1, list2)
print(print_linked_list(merged))  # Output: 1 -> 1 -> 2 -> 3 -> 4 -> 4