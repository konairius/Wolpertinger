'''
Created on Jan 24, 2013

'''

import logging
logger = logging.getLogger(__name__)

import hashlib
import os
import shelve

import WTConfig

fileCounter = 0


class File(object):
    '''
    Represents a File in wolpertinger,
    don't use the constructor, use the fromPath method
    it will Cache the hashes
    '''
    @classmethod
    def fromPath(cls, path):
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
            lib[path] = cls(path)
        fileCounter += 1
        return lib[path]

    def __init__(self, path):
        '''
        DONT'T USE: Use Factory instead!
        '''
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
            logger.warning(self.path + ' exists on both ends!')
        return syncList

    def getPath(self):
        return self.path

    def getMtime(self):
        return self.mtime

    def getSize(self):
        return self.size

    def getHash(self):
        return self.hash

    @staticmethod
    def createHash(path):
        logger.debug('Creating new hash for ' + path)
        sha1 = hashlib.sha1()
        with open(path, 'rb') as data:
            for chunk in iter(lambda: data.read(128 * sha1.block_size), b''):
                sha1.update(chunk)
        return str(sha1.hexdigest())


class Folder(object):
    '''
    Represents an entire folder,
    will crate File objects for the entire subtree,
    use it with caution.
    '''
    @classmethod
    def fromPath(cls, path):
        return cls(path)

    def __init__(self, path):
        self.config = WTConfig.getConfig()
        if path not in self.config.getExposedFolders().values():
            raise TargetNotExposedError(path)
        self.items = dict()
        self.path = path
        for item in os.listdir(path):
            if os.path.isdir(os.path.join(path, item)):
                self.items[item] = Folder(os.path.join(path, item))
            elif os.path.isfile(os.path.join(path, item)):
                self.items[item] = File.fromPath(os.path.join(path, item))

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
                localPath = self.items[key].getPath()
                remotePath = os.path.join(folder.getPath(), (os.path.relpath(self.items[key].getPath(), self.path)))
                syncList.append((localPath, remotePath))
        if twoWay:
            syncList += folder.sync(self, False)

        return syncList

    def getItems(self):
        return self.items

    def getPath(self):
        return self.path


class FileChangedError(Exception):
    pass


class TargetNotExposedError(Exception):
    pass
