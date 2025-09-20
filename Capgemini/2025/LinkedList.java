class LinkedList {
    // Node class for linked list
    class Node {
        int data;
        Node next;
        
        public Node(int data) {
            this.data = data;
            this.next = null;
        }
    }
    
    private Node head;
    
    // Constructor
    public LinkedList() {
        this.head = null;
    }
    
    // Add a node at the end
    public void append(int data) {
        if (head == null) {
            head = new Node(data);
            return;
        }
        
        Node current = head;
        while (current.next != null) {
            current = current.next;
        }
        current.next = new Node(data);
    }
    
    // Add a node at the beginning
    public void prepend(int data) {
        Node newNode = new Node(data);
        newNode.next = head;
        head = newNode;
    }
    
    // Insert a node after a given node
    public void insertAfter(Node prevNode, int data) {
        if (prevNode == null) {
            System.out.println("The given previous node cannot be null");
            return;
        }
        
        Node newNode = new Node(data);
        newNode.next = prevNode.next;
        prevNode.next = newNode;
    }
    
    // Delete a node with given key
    public void deleteNode(int key) {
        Node temp = head, prev = null;
        
        // If head node itself holds the key to be deleted
        if (temp != null && temp.data == key) {
            head = temp.next;
            return;
        }
        
        // Search for the key to be deleted
        while (temp != null && temp.data != key) {
            prev = temp;
            temp = temp.next;
        }
        
        // If key was not present in linked list
        if (temp == null) return;
        
        // Unlink the node from linked list
        prev.next = temp.next;
    }
    
    // Search a node
    public boolean search(int key) {
        Node current = head;
        while (current != null) {
            if (current.data == key) {
                return true;
            }
            current = current.next;
        }
        return false;
    }
    
    // Print the linked list
    public void printList() {
        Node current = head;
        System.out.print("LinkedList: ");
        while (current != null) {
            System.out.print(current.data + " ");
            current = current.next;
        }
        System.out.println();
    }
    
    // Get the size of linked list
    public int size() {
        int count = 0;
        Node current = head;
        while (current != null) {
            count++;
            current = current.next;
        }
        return count;
    }
    
    // Get node at specific index
    public Node getAt(int index) {
        Node current = head;
        int count = 0;
        
        while (current != null) {
            if (count == index) {
                return current;
            }
            count++;
            current = current.next;
        }
        
        return null;
    }
    
    // Main method for testing
    public static void main(String[] args) {
        LinkedList list = new LinkedList();
        
        // Append elements
        list.append(1);
        list.append(2);
        list.append(3);
        list.printList();
        
        // Prepend element
        list.prepend(0);
        list.printList();
        
        // Insert after second node
        list.insertAfter(list.getAt(1), 5);
        list.printList();
        
        // Delete node
        list.deleteNode(2);
        list.printList();
        
        // Search
        System.out.println("Search for 5: " + list.search(5));
        System.out.println("Search for 2: " + list.search(2));
        
        // Size
        System.out.println("Size of linked list: " + list.size());
    }
}
