'''
Created on Jan 24, 2013

'''

import logging
logger = logging.getLogger(__name__)

import os
from os import listdir
from abc import ABCMeta, abstractmethod

from WTConfig import getConfig
from Util.WTUri import Uri
from Util.WTHasher import getHasher
from Util.WTHasher import NotYetCreatedError


class Item(metaclass=ABCMeta):
    @property
    @abstractmethod
    def path(self):
        '''
        Returns the pysical path of the item
        '''
        pass

    @property
    @abstractmethod
    def uri(self):
        '''
        Returns the logical Uri inside the Wolpertinger system
        '''
        pass

    @property
    @abstractmethod
    def size(self):
        '''
        Return the size of the underlying structure or file.
        '''
        pass

    @property
    @abstractmethod
    def mtime(self):
        '''
        Returns the latest mtime of the underlying structure
        '''
        pass

    @property
    @abstractmethod
    def hasHash(self):
        '''
        Return if every element underlying structure has been Hashed.
        '''
        pass

    @abstractmethod
    def sync(self, other):
        '''
        Returns a list of Files or Folders that need to be copied
        the sync the underlying structures.
        '''
        pass

    @abstractmethod
    def matches(self, other):
        '''
        Returns True if the Items seem to have the same content
        '''
        pass

    def getItem(self, uri):
        if self.uri == uri:
            if self.hasHash:
                return self
            else:
                return self.__class__(self.path, self.uri, sync=True)

        if not self.uri.contains(uri):
            raise TargetNotExposedError(uri)

        else:
            return self.items[uri.getNextItem(self.uri)].getItem(uri)


class File(Item):
    '''
    Represents a File in Wolpertinger,
    don't use the constructor, use the fromPath method
    it will Cache the hashes
    '''

    def __init__(self, path, uri, sync=True):
        '''
        DONT'T USE: Use Factory instead!
        '''
        self._uri = uri
        self._path = path
        self._size = os.path.getsize(path)
        self._mtime = os.path.getmtime(path)
        try:
            self._hash = getHasher().hashFile(self, sync).hash
        except NotYetCreatedError as e:
            if not sync:
                pass
            else:
                raise AttributeError(e)

    @property
    def path(self):
        '''
        Returns the pysical path of the item
        '''
        return self._path

    @property
    def uri(self):
        '''
        Returns the logical Uri inside the Wolpertinger system
        '''
        return self._uri

    @property
    def size(self):
        '''
        Return the size of the underlying structure or file.
        '''
        return self._size

    @property
    def mtime(self):
        '''
        Returns the latest mtime of the underlying structure
        '''
        return self._mtime

    @property
    def hash(self):
        '''
        Returns the hash of the file
        '''
        try:
            return self._hash
        except AttributeError as e:
            raise NotYetCreatedError(e)

    @hash.setter
    def hash(self, value):
        self._hash = value

    @property
    def hasHash(self):
        '''
        Return if every element underlying structure has been Hashed.
        '''
        try:
            self.hash
            return True
        except NotYetCreatedError:
            return False

    def sync(self, other):
        '''
        Returns a list of Files or Folders that need to be copied
        the sync the underlying structures.
        '''
        if self.matches(other):
            return ((self.uri(), other.uri()))

    def matches(self, other):
        '''
        Returns True if the Items seem to have the same content
        '''
        if self.hash == other.hash:
            return True
        return False


class Folder(Item):
    '''
    Represents an entire folder,
    will crate File objects for the entire subtree,
    use it with caution.
    '''

    def __init__(self, path, uri, sync=True):
        self.config = getConfig()
        self._items = dict()
        self._path = path
        self._uri = uri
        self._mtime = os.path.getmtime(path)
        for item in listdir(path):
            try:
                if os.path.isdir(os.path.join(path, item)):
                    self.items[item] = Folder(os.path.join(path, item), self.uri.append(item), sync)
                elif os.path.isfile(os.path.join(path, item)):
                    self.items[item] = File(os.path.join(path, item), self.uri.append(item), sync)
            except Exception as e:
                logger.error(str(uri.append(item)) + ': ' + str(e))

    @property
    def path(self):
        '''
        Returns the pysical path of the item
        '''
        return self._path

    @property
    def uri(self):
        '''
        Returns the logical Uri inside the Wolpertinger system
        '''
        return self._uri

    @property
    def items(self):
        '''
        The items in the Folder, using the name as key
        '''
        return self._items

    @property
    def size(self):
        '''
        Return the size of the underlying structure or file.
        '''
        size = 0
        for key in self.items.keys():
            size += self.items[key].size

    @property
    def mtime(self):
        '''
        Returns the latest mtime of the underlying structure
        '''
        mtime = self._mtime
        for key in self.items.keys():
            kmtime = self.items[key].mtime
            if kmtime > mtime:
                mtime = kmtime
        return mtime

    @property
    def hasHash(self):
        '''
        Return if every element underlying structure has been Hashed.
        '''
        for key in self.items.keys():
            if not self.items[key].hasHash:
                return False
            return True

    def sync(self, other):
        '''
        Returns a list of Files or Folders that need to be copied
        the sync the underlying structures.
        '''
        syncList = []
        for key in self.items.keys():
            try:
                syncList += self.items[key].sync(other.items[key])
            except KeyError:
                syncList.append((str(self.items[key].uri), str(other.uri)))
        return syncList

    def matches(self, other):
        '''
        Returns True if the Items seem to have the same content
        '''
        try:
            for key in self.items.keys():
                if not self.items[key].matches(other.items[key]):
                    return False
                return True
        except (KeyError, AttributeError):
            return False


class Export(object):
    '''
    Represents an Export root
    '''
    def __init__(self, path, name):
        self.config = getConfig()
        self.rootUri = Uri('WT://export.' + name + '.' + self.config.getServicename() + '/')
        self.path = path
        self.name = name
        self.refresh(sync=False)

    def refresh(self, sync=True):
        logger.info('Checking cache for: ' + self.path)
        self.rootItem = Folder(self.path, self.rootUri, sync)

    def getItem(self, uri):
        return self.rootItem.getItem(uri)

    def getRootUri(self):
        return self.rootUri


class TargetNotExposedError(Exception):
    pass
