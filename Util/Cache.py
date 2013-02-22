'''
Created on Feb 3, 2013

@author: konsti
'''

import logging
logger = logging.getLogger(__name__)


import shelve
from threading import Semaphore
from os.path import isfile

from abc import ABCMeta, abstractmethod


from Util.Config import config


def cache():
    global _cache
    try:
        return _cache
    except NameError:
        _cache = Cache()
        return _cache


class Cacheable(metaclass=ABCMeta):
    @property
    @abstractmethod
    def version(self):
        '''
        Should retrun an version that changes, at least, every time the data fromat changes.
        '''
        pass

    @abstractmethod
    def upgrade(self, item):
        '''
        gets the Cached version of the item, should return the upgraded version of the item
        '''

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
        if not isinstance(item, Cacheable):
            raise NotCacheableError(item)
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
            
    def delete(self, item):
        if not isinstance(item, Cacheable):
            raise NotCacheableError(item)
        try:
            self.writeSemaphore.acquire(blocking=True)
            cache = shelve.open(self.cachePath, writeback=False)
            key = self.getKey(item)
            del cache[key]
        except IOError as e:
            raise CacheNotAvailableError(e)
        finally:
            cache.close()
            self.writeSemaphore.release()

    def get(self, item):
        if not isinstance(item, Cacheable):
            logger.error('Item is not Cacheable: ' + str(item))
            raise NotCacheableError(item)
        try:
            cache = shelve.open(self.cachePath, writeback=False)
            key = self.getKey(item)
            cacheItem = cache[key]
            if not cacheItem.version == item.version:
                try:
                    self.add(item.upgrade(cacheItem))
                    return self.get(item)
                except NotUpgradableError:
                    self.delete(item)
                    logger.warning('Cached version missmatch: was ' + str(cacheItem.version) + ' excpected ' + str(item.version))
                    raise ItemVersionMissmatchError(item)
        except KeyError as e:
            raise NotInCacheError(e)
        except IOError as e:
            raise CacheNotAvailableError(e)
        finally:
            cache.close()
        return cacheItem

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
            logger.error('Expected version ' + str(CacheVersion.version))
            raise CacheVersionMissmatch(cacheVersion.version)

    @staticmethod
    def getKey(item):
        return repr(item)


class CacheVersion(Cacheable):
    def __init__(self):
        self._version = 1.1

    @property
    def version(self):
        return self._version

    def __eq__(self, other):
        return self.version == other.version

    def __repr__(self):
        return str(self.__class__)

    def __str__(self):
        return 'Version: ' + str(self.version)
    
    def upgrade(self):
        raise NotUpgradableError


class NotInCacheError(Exception):
    pass


class NotCacheableError(Exception):
    pass


class CacheNotAvailableError(Exception):
    pass


class CacheVerificationError(Exception):
    pass


class CacheVersionMissmatch(Exception):
    pass


class ItemVersionMissmatchError(Exception):
    pass

class NotUpgradableError(Exception):
    pass
