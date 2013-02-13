'''
Created on Feb 3, 2013

@author: konsti
'''

import logging
logger = logging.getLogger(__name__)


import shelve
from threading import Semaphore
from os.path import isfile


from Util.Config import config


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

        self.verify()

    def add(self, item):
        try:
            self.writeSemaphore.acquire(blocking=True)
            cache = shelve.open(self.cachePath, writeback=False)
            key = self.getKey(item)
            cache[key] = item
        except IOError as e:
            raise CacheNotAvailableError(e)
        finally:
            cache.close()
            self.writeSemaphore.release()

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

    def verify(self):
        if not isfile(self.cachePath):
            self.add(CacheVersion())

        try:
            cacheVersion = self.get(CacheVersion())
        except NotInCacheError as e:
            logger.error('Cache dosn\'t contain Version')
            raise CacheVerificationError(e)

        if not cacheVersion == CacheVersion():
            logger.error('Cache has version ' + str(cacheVersion.version))
            logger.error('Excpected version ' + str(CacheVersion.version))
            raise CacheVersionMissmatch(cacheVersion.version)

    @staticmethod
    def getKey(item):
        return repr(item.__class__) + ':' + repr(item)


class CacheVersion(object):
    def __init__(self):
        self._version = 1.0

    @property
    def version(self):
        return self._version

    def __eq__(self, other):
        return self.version == other.version

    def __repr__(self):
        return self.__class__


class NotInCacheError(Exception):
    pass


class CacheNotAvailableError(Exception):
    pass


class CacheVerificationError(Exception):
    pass


class CacheVersionMissmatch(Exception):
    pass
