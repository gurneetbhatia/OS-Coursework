import queue
import hashlib
from random import randrange


# Various implementations of caching.
class Memory:
    def __init__(self):
        self.hit_count = 0

    def get_hit_count(self):
        return self.hit_count

    def name(self):
        return "Memory"

    def lookup(self, address):
        # This one actually has no cache, so every lookup
        # requires a memory hit.
        print("Memory Access", end=" ")
        self.hit_count += 1
        string = str(address ^ 3).encode()
        return hashlib.md5(string).hexdigest()[:8]


class CyclicCache(Memory):
    def name(self):
        return "Cyclic"

    # Edit the code below to provide an implementation of a cache that
    # uses a cyclic caching strategy with a cache size of 4. You can
    # use additional methods and variables as you see fit as long as you
    # provide a suitable overridding of the lookup method.

    def lookup(self, address):
        cacheAddresses = [x[0] for x in self.cache]
        cacheData = [x[1] for x in self.cache]
        if address not in cacheAddresses:
            # memory hit since address not in cache
            self.cache[self.nextPos - 1] = (address, super().lookup(address))
            self.nextPos = self.nextPos + 1 if self.nextPos < 4 else 1
            cacheAddresses = [x[0] for x in self.cache]
            cacheData = [x[1] for x in self.cache]
        return cacheData[cacheAddresses.index(address)]

    def __init__(self):
        super().__init__()
        self.nextPos = 1
        self.cache = [(None, None), (None, None), (None, None), (None, None)]


class LRUCache(Memory):
    def name(self):
        return "LRU"

    # Edit the code below to provide an implementation of a cache that
    # uses a least recently used caching strategy with a cache size of
    # 4. You can use additional methods and variables as you see fit as
    # long as you provide a suitable overridding of the lookup method.

    def lookup(self, address):
        cacheAddresses = [x[0] for x in self.cache]
        cacheData = [x[1] for x in self.cache]
        if address not in cacheAddresses:
            #self.hit_count += 1
            self.cache = self.cache[1:]
            self.cache.append((address, super().lookup(address)))
            cacheAddresses = [x[0] for x in self.cache]
            cacheData = [x[1] for x in self.cache]
        else:
            index = cacheAddresses.index(address)
            self.cache = self.cache[0:index] + self.cache[index+1:]
            self.cache.append((address, cacheData[index]))
        return cacheData[cacheAddresses.index(address)]

    def __init__(self):
        super().__init__()
        self.cache = [(None, None), (None, None), (None, None), (None, None)]
