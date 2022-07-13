from __future__ import annotations
from typing import Dict, Optional


"""
Least Recently Used (LRU) cache. It has O(1) amortized performance for every operation.

API:
    - get(key: int) -> int
    - put(key: int, value: int)
    - get_most_recently_used() -> int
    - get_least_recently_used() -> int
"""


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next: Optional[Node] = None
        self.prev: Optional[Node] = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.cache: Dict[int, Node] = {}

    def get(self, key):
        """
        Get the value of the key if it exists, otherwise return -1.
        """
        if key in self.cache:
            node = self.cache[key]
            self.remove(node)
            self.add(node)
            return node.value
        return -1
    
    def get_most_recently_used(self):
        """
        Get the key of the most recently used item in the cache.
        """
        return self.tail.prev.key
    
    def get_least_recently_used(self):
        """
        Get the key of the least recently used item in the cache.
        """
        return self.head.next.key

    def put(self, key, value):
        """
        Add the key-value pair to the cache. If the key already exists, update the value.
        """
        if key in self.cache:
            self.remove(self.cache[key])
        node = Node(key, value)
        self.add(node)
        self.cache[key] = node
        if len(self.cache) > self.capacity:
            node = self.head.next
            self.remove(node)
            del self.cache[node.key]

    def add(self, node: Node):
        """
        Add the node to the end of the list.
        """
        p = self.tail.prev
        p.next = node
        self.tail.prev = node
        node.prev = p
        node.next = self.tail

    def remove(self, node: Node):
        """
        Remove the node from the list.
        """
        p = node.prev
        n = node.next
        p.next = n
        n.prev = p
        
    def __str__(self):
        return str(self.cache)
        
if __name__ == "__main__":
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    print(cache.get(1))
    cache.put(3, 3)
    print(cache.get(2))
    cache.put(4, 4)
    print(cache.get(1))
    print(cache.get(3))
    print(cache.get(4))
    cache.put(4, 5)
    cache.put(3, 6)
    print(cache)
    print(cache.get_most_recently_used())
    print(cache.get_least_recently_used())