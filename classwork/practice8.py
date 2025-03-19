class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

def reverse_list(head):
    prev = None
    current = head
    while current:
        nxt = current.next
        current.next = prev
        prev = current
        current = nxt
    return prev