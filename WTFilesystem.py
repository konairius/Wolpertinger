'''
Created on Jan 24, 2013

'''

import logging
logger = logging.getLogger(__name__)

import hashlib
import os
import shelve

import WTConfig
from Util.WTUri import Uri

fileCounter = 0


class Item(object):
    def getItem(self, uri):
        if self.uri == uri:
            return self

        if not self.uri.contains(uri):
            raise TargetNotExposedError(uri)

        else:
            return self.items[uri.getNextItem(self.uri)].getItem(uri)


class File(Item):
    '''
    Represents a File in wolpertinger,
    don't use the constructor, use the fromPath method
    it will Cache the hashes
    '''
    @classmethod
    def fromPath(cls, path, uri):
        global fileCounter
        config = WTConfig.getConfig()
        lib = shelve.open(config.getFileCache())
        size = os.path.getsize(path)
        mtime = os.path.getmtime(path)
        try:
            if not lib[path].size == size and lib[path].mtime == mtime:
                raise FileChangedError
            logger.debug('Cache hit for Path: ' + path)
        except (FileChangedError, KeyError):
            logger.debug('Cache miss for Path:' + path)
            lib[path] = cls(path, uri)
        fileCounter += 1
        return lib[path]

    def __init__(self, path, uri):
        '''
        DONT'T USE: Use Factory instead!
        '''
        self.uri = uri
        self.path = path
        self.hash = File.createHash(path)
        self.size = os.path.getsize(path)
        self.mtime = os.path.getmtime(path)

    def matches(self, file):
        try:
            if self.hash == file.getHash():
                return True
            return False
        except (KeyError, AttributeError):
            return False

    def sync(self, file):
        syncList = []
        if self.matches(file):
            pass
        else:
            logger.warning('Conflict Found:')
            logger.warning(self.uri.string + ' exists on both ends!')
        return syncList

    def getPath(self):
        return self.path

    def getMtime(self):
        return self.mtime

    def getSize(self):
        return self.size

    def getHash(self):
        return self.hash

    def getUri(self):
        return self.uri

    @staticmethod
    def createHash(path):
        logger.debug('Creating new hash for ' + path)
        sha1 = hashlib.sha1()
        with open(path, 'rb') as data:
            for chunk in iter(lambda: data.read(128 * sha1.block_size), b''):
                sha1.update(chunk)
        return str(sha1.hexdigest())


class Folder(Item):
    '''
    Represents an entire folder,
    will crate File objects for the entire subtree,
    use it with caution.
    '''

    def __init__(self, path, uri):
        self.config = WTConfig.getConfig()
        #if path not in self.config.getExposedFolders().values():
        #    raise TargetNotExposedError(path)
        self.items = dict()
        self.path = path
        self.uri = uri
        for item in os.listdir(path):
            try:
                if os.path.isdir(os.path.join(path, item)):
                    self.items[item] = Folder(os.path.join(path, item), self.uri.append(item))
                elif os.path.isfile(os.path.join(path, item)):
                    self.items[item] = File.fromPath(os.path.join(path, item), self.uri.append(item))
            except Exception as e:
                logger.error(uri + ': ' + e)

    def matches(self, folder):
        '''
        Quickly checks recursive if the Folders are matching.
        '''
        try:
            for key in self.items.keys():
                if not self.items[key].matches(folder.getItems()[key]):
                    return False
                return True
        except (KeyError, AttributeError):
            return False

    def sync(self, folder, twoWay=False):
        syncList = []
        for key in self.items.keys():
            try:
                syncList += self.items[key].sync(folder.getItems()[key])
            except KeyError:
                #localPath = self.items[key].getPath()
                #remotePath = os.path.join(folder.getPath(), (os.path.relpath(self.items[key].getPath(), self.path)))
                syncList.append((self.items[key].getUri().string, folder.getUri().string))
        if twoWay:
            syncList += folder.sync(self, False)

        return syncList

    def getItems(self):
        return self.items

    def getPath(self):
        return self.path

    def getUri(self):
        return self.uri


class Export(object):
    '''
    Represents an Export root
    '''
    def __init__(self, path, name):
        self.config = WTConfig.getConfig()
        self.rootUri = Uri('WT://export.' + name + '.' + self.config.getServicename() + '/')
        self.path = path
        self.name = name

    def refresh(self):
        logger.info('Updating cache for: ' + self.path)
        self.rootItem = Folder(self.path, self.rootUri)

    def getItem(self, uri):
        return self.rootItem.getItem(uri)

    def getRootUri(self):
        return self.rootUri


class FileChangedError(Exception):
    pass


class TargetNotExposedError(Exception):
    pass
