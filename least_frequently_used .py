from __future__ import annotations
from typing import Dict, Optional


"""
Least Frequently Used (LFU) cache.

API: 
    - get(key: int) -> int
    - set(key: int, value: int)
    - get_most_frequently_used() -> int
"""


class Node:
    """
    Linked List node implementation. Additionally, we store the frequency of the node.
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None
        self.freq = 1


class DoublyLinkedList:
    """
    Doubly linked list implementation.
    """
    def __init__(self):
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def add_node(self, node: Node):
        """
        Add a node to the head of the list.
        """
        node.prev = self.head
        node.next = self.head.next

        self.head.next.prev = node
        self.head.next = node

        self.size += 1

    def remove_node(self, node: Node):
        """
        Remove a node from the list.
        """
        node.prev.next = node.next
        node.next.prev = node.prev

        self.size -= 1

    def remove_tail(self):
        """
        Remove the tail node from the list.
        """
        node = self.tail.prev
        self.remove_node(node)
        return node

    def move_to_head(self, node):
        """
        Move a node to the head of the list.
        """
        self.remove_node(node)
        self.add_node(node)


class LFUCache:
    """
    Least Frequently Used (LFU) cache.
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.size = 0
        self.key_to_node: Dict[int, Node] = {} # Key to node mapping
        self.freq_to_dll: Dict[int, DoublyLinkedList] = {} # Frequency to doubly linked list mapping
        self.min_freq = 0

    def get(self, key):
        if key not in self.key_to_node:
            return -1

        node = self.key_to_node[key]
        freq = node.freq
        self.freq_to_dll[freq].remove_node(node)

        if freq == self.min_freq and self.freq_to_dll[freq].size == 0:
            self.min_freq += 1

        if freq + 1 not in self.freq_to_dll:
            self.freq_to_dll[freq + 1] = DoublyLinkedList()

        self.freq_to_dll[freq + 1].add_node(node)
        node.freq += 1

        return node.value

    def set(self, key, value):
        if self.capacity == 0:
            return

        if key in self.key_to_node:
            node = self.key_to_node[key]
            node.value = value
            self.get(key)
            return

        if self.size == self.capacity:
            node = self.freq_to_dll[self.min_freq].remove_tail()
            del self.key_to_node[node.key]
            self.size -= 1

        node = Node(key, value)
        node.freq = 1
        self.key_to_node[key] = node

        if 1 not in self.freq_to_dll:
            self.freq_to_dll[1] = DoublyLinkedList()

        self.freq_to_dll[1].add_node(node)
        self.min_freq = 1
        self.size += 1
        
    def get_most_freq_node(self):
        return self.freq_to_dll[self.min_freq].head.next.key, self.freq_to_dll[self.min_freq].head.next.value
        
if __name__ == "__main__":
    cache = LFUCache(2)
    cache.set(1, 1)
    cache.set(2, 2)
    print(cache.get(1))  # returns 1
    cache.set(3, 3)  # evicts key 2
    print(cache.get(2))  # returns -1 (not found)
    print(cache.get(3))  # returns 3
    cache.set(4, 4)  # evicts key 1
    print(cache.get(1))  # returns -1 (not found)
    print(cache.get(3))  # returns 3
    print(cache.get(4))  # returns 4
    cache.set(5, 5)  # evicts key 3
    print(cache.get(3))  # returns -1 (not found)
    print(cache.get(4))  # returns 4
    print(cache.get(5))  # returns 5
    cache.set(6, 6)  # evicts key 4
    print(cache.get(4))  # returns -1 (not found)
    print(cache.get(5))  # returns 5
    print(cache.get(6))  # returns 6
    cache.set(7, 7)  # evicts key 5
    print(cache.get(5))  # returns -1 (not found)
    print(cache.get(6))  # returns 6
    print(cache.get(7))  # returns 7
    cache.set(8, 8)  # evicts key 6
    print(cache.get(6))  # returns -1 (not found)
    print(cache.get(7))  # returns 7
    print(cache.get(8))  # returns 8
    cache.set(9, 9)  # evicts key 7
    print(cache.get(7))  # returns -1 (not found)
    print(cache.get(8))  # returns 8
    print(cache.get(9))  # returns 9
    cache.set(10, 10)  # evicts key 8
    print(cache.get(8))  # returns -1 (not found)
    cache.set(9, 11)
    print(cache.get_most_freq_node())  # returns 9