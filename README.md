# LRU & LFU Cache

In this repo i treid to implement a LRU (Least Recently Used) and LFU (Least Frequently Used) cache. Thay both have amoritized O(1) access time in theory.

LRU cache is a cache where the least recently used item is removed when the cache is full.

LFU cache is a cache where the least frequently used item is removed when the cache is full.

They both have similar APIs:

``` python
get(key: int) -> int
put(key: int, value: int) # or set(key: int, value: int)
get_most_recently_used(key: int) -> int # or set_most_recently_used(key: int)
get_least_frequently_used(key: int) -> int
```