"""
The class should have the following methods:

set(key, value) - sets key to value. If there are already n items in the cache and we are adding a new item,
                  then it should also remove the least frequently used item. If there is a tie, 
                  then the least recently used key should be removed.
get(key) - gets the value at key. If no such key exists, return null.
Each operation should run in O(1) time.

"""
from __future__ import annotations
import heapq
from typing import Dict, List


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.freq = 0
        self.time = 0

    def __lt__(self, other: Node):
        if self.freq == other.freq:
            return self.time < other.time
        return self.freq < other.freq

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.time = 0
        self.cache: Dict[int, Node] = {}
        self.heap: List[Node] = []

    def set(self, key, value):
        self.time = 1
        if key in self.cache:
            self.cache[key].value = value
            self.cache[key].freq = 1
            self.cache[key].time = self.time
            heapq.heapify(self.heap)
        else:
            if len(self.cache) == self.capacity:
                node = heapq.heappop(self.heap)
                del self.cache[node.key]
            node = Node(key, value)
            node.freq = 1
            node.time = self.time
            self.cache[key] = node
            heapq.heappush(self.heap, node)

    def get(self, key):
        if key not in self.cache:
            return None
        self.time = 1
        self.cache[key].freq = 1
        self.cache[key].time = self.time
        heapq.heapify(self.heap)
        return self.cache[key].value

    def get_most_frequent(self):
        if len(self.heap) == 0:
            return None
        return self.heap[0].key, self.heap[0].value

if __name__ == '__main__':
    cache = LFUCache(2)
    cache.set(1, 1)
    cache.set(2, 2)
    print(cache.get(1))
    cache.set(3, 3)
    print(cache.get(2))
    print(cache.get(3))
    cache.set(4, 4)
    print(cache.get(1))
    print(cache.get(3))
    print(cache.get(4))