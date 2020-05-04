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
        # This one actually has no cache, so every lookup requires
        # a memory hit.
        print("Memory Access", end=" ")
        self.hit_count += 1
        string = str(address ^ 3).encode()
        return hashlib.md5(string).hexdigest()[:8]


class CyclicCache(Memory):

    def __init__(self, size=4):
        super().__init__()
        # The cache
        self.cache = {}
        # The cache size.
        self.cache_size = size
        # A queue of keys that are in the cache. This will be used to
        # work out which slot to evict. Use of the queue corresponds to
        # cyclic behaviour.
        self.cached_keys = queue.Queue(self.cache_size)

    def name(self):
        return "Cyclic"

    '''If the value is in the cache, get it and return it. Otherwise,
    get the value from memory and return it'''
    def lookup(self, address):
        # Is it in the cache? If so, return.
        if address in self.cache:
            return self.cache[address]
        else:
            # Is the Cache full?
            if self.cached_keys.full():
                # Grab the key that was added to the key first,
                # this will be the next one for removal.
                removal = self.cached_keys.get()
                # Evict from the cache.
                del self.cache[removal]
            # There should be a free space now.
            value = super().lookup(address)
            # Cache the value and push the key onto the queue.
            self.cache[address] = value
            self.cached_keys.put(address)
            return value


class LRUCache(Memory):
    def __init__(self, size=4):
        super().__init__()
        # The cache.
        self.cache = {}
        # The cache size.
        self.cache_size = size
        # A list of keys that are in the cache. This will be used to work out
        # which slot to evict. The least recently used is on the front of the
        # queue
        self.cached_keys = []

    def name(self):
        return "LRU"

    '''If the value is in the cache, get it and return it. Otherwise,
    get the value from memory and return it'''
    def lookup(self, address):
        # Is it in the cache? If so, return
        if address in self.cache:
            #        print("    {}".format(cache))
            # mark the address as being the most recently used, i.e.
            # send to end of list
            self.cached_keys.remove(address)
            self.cached_keys.append(address)
            return self.cache[address]
        else:
            # Is the Cache full?
            if len(self.cached_keys) >= self.cache_size:
                # Find the key that is least recently used. It'll be the
                # one at the beginning of the list
                removal = self.cached_keys[0]
                # Remove it from the list of cached keys.
                self.cached_keys = self.cached_keys[1:]
                # Evict from the cache
                del self.cache[removal]
            # There should be a free space now.
            value = super().lookup(address)
            # Cache the value and push the key onto the queue.
            self.cache[address] = value
            # add to the list, thus marking the address as being the most
            # recently used
            self.cached_keys.append(address)
            return value


class RandomCache(Memory):
    def __init__(self, size=4):
        super().__init__()

        # The cache.
        self.cache = {}
        # The cache size.
        self.cache_size = size
        # A list of keys that are in the cache. This will be used to work out
        # which slot to evict.
        self.cached_keys = []

    def name(self):
        return "Random"

    '''If the value is in the cache, get it and return it. Otherwise,
    get the value from memory and return it'''
    def lookup(self, address):
        # Is it in the cache? If so, return
        if address in self.cache:
            # mark the address as being the most recently used, i.e. send
            # to end of list
            self.cached_keys.remove(address)
            self.cached_keys.append(address)
            return self.cache[address]
        else:
            # Is the Cache full?
            if len(self.cached_keys) >= self.cache_size:
                # Grab a random key
                evictee = randrange(0, self.cache_size)
                removal = self.cached_keys[evictee]
                # Remove it from the list of cached keys.
                self.cached_keys.remove(removal)
                # Evict from the cache
                del self.cache[removal]
            # There should be a free space now.
            value = super().lookup(address)
            # Cache the value and push the key onto the queue.
            self.cache[address] = value
            # add to the list, thus marking the address as being the most
            # recently used
            self.cached_keys.append(address)
            return value
