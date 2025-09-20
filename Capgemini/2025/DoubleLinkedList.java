public class DoubleLinkedList<E> {
    
    private static class Node<E> {
        E element;
        Node<E> prev;
        Node<E> next;
        
        public Node(E element, Node<E> prev, Node<E> next) {
            this.element = element;
            this.prev = prev;
            this.next = next;
        }
    }
    
    private Node<E> head;
    private Node<E> tail;
    private int size;
    
    public DoubleLinkedList() {
        head = null;
        tail = null;
        size = 0;
    }
    
    public int size() {
        return size;
    }
    
    public boolean isEmpty() {
        return size == 0;
    }
    
    public void addFirst(E element) {
        Node<E> newNode = new Node<>(element, null, head);
        if (head != null) {
            head.prev = newNode;
        } else {
            tail = newNode;
        }
        head = newNode;
        size++;
    }
    
    public void addLast(E element) {
        Node<E> newNode = new Node<>(element, tail, null);
        if (tail != null) {
            tail.next = newNode;
        } else {
            head = newNode;
        }
        tail = newNode;
        size++;
    }
    
    public E removeFirst() {
        if (isEmpty()) {
            return null;
        }
        
        E element = head.element;
        head = head.next;
        
        if (head != null) {
            head.prev = null;
        } else {
            tail = null;
        }
        
        size--;
        return element;
    }
    
    public E removeLast() {
        if (isEmpty()) {
            return null;
        }
        
        E element = tail.element;
        tail = tail.prev;
        
        if (tail != null) {
            tail.next = null;
        } else {
            head = null;
        }
        
        size--;
        return element;
    }
    
    public void display() {
        Node<E> current = head;
        while (current != null) {
            System.out.print(current.element + " <-> ");
            current = current.next;
        }
        System.out.println("null");
    }
}
