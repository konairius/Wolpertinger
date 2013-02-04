'''
Created on Feb 3, 2013

@author: konsti
'''

import shelve
from threading import Semaphore


from WTConfig import config


def cache():
    global _cache
    try:
        return _cache
    except NameError:
        _cache = Cache()
        return _cache


class Cache(object):
    '''
    Class used to persistently safe hashes and other elements (if needed)
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.cachePath = config().cachePath
        self.writeSemaphore = Semaphore()

    def add(self, item):
        try:
            self.writeSemaphore.acquire(blocking=True)
            cache = shelve.open(self.cachePath, writeback=False)
            key = self.getKey(item)
            cache[key] = item
        except IOError as e:
            raise CacheNotAvailableError(e)
        finally:
            self.writeSemaphore.release()
            cache.close()

    def get(self, item):
        try:
            cache = shelve.open(self.cachePath, writeback=False)
            key = self.getKey(item)
            item = cache[key]
        except KeyError as e:
            raise NotInCacheError(e)
        except IOError as e:
            raise CacheNotAvailableError(e)
        finally:
            cache.close()
        return item

    @staticmethod
    def getKey(item):
        return repr(item.__class__) + ':' + repr(item)


class NotInCacheError(Exception):
    pass


class CacheNotAvailableError(Exception):
    pass
