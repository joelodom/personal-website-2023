import memcache

class MemcachedClient:
    def __init__(self, server='localhost:11211'):
        self.client = memcache.Client([server])

    def get(self, key):
        return self.client.get(key)

    def set(self, key, value, expire=0):
        '''Expire is in seconds.'''
        return self.client.set(key, value, expire)

    def delete(self, key):
        return self.client.delete(key)

