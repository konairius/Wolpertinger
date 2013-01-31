'''
Created on Jan 24, 2013

'''

import logging
logger = logging.getLogger(__name__)

import os
from os import listdir

from WTConfig import getConfig
from Util.WTUri import Uri
from Util.WTHasher import getHasher

fileCounter = 0


class Item(object):
    def getItem(self, uri):
        if self.uri == uri:
            if self.hasHash():
                return self
            else:
                return self.__class__(self.path, self.uri, sync=True)

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

    def __init__(self, path, uri, sync=True):
        '''
        DONT'T USE: Use Factory instead!
        '''
        self.uri = uri
        self.path = path
        self.size = os.path.getsize(path)
        self.mtime = os.path.getmtime(path)
        try:
            self.hash = getHasher().hashFile(self, sync).hash
        except AttributeError:
            pass

    def matches(self, file):
        try:
            if self.hash == file.hash:
                return True
            return False
        except AttributeError:
            return False

    def sync(self, file):
        syncList = []
        if self.matches(file):
            pass
        else:
            logger.warning(self.uri.string + ' exists on both ends but dosn\'t Match')
        return syncList

    def hasHash(self):
        try:
            self.hash
            return True
        except AttributeError:
            return False


class Folder(Item):
    '''
    Represents an entire folder,
    will crate File objects for the entire subtree,
    use it with caution.
    '''

    def __init__(self, path, uri, sync=True):
        self.config = getConfig()
        #if path not in self.config.getExposedFolders().values():
        #    raise TargetNotExposedError(path)
        self.items = dict()
        self.path = path
        self.uri = uri
        for item in listdir(path):
            try:
                if os.path.isdir(os.path.join(path, item)):
                    self.items[item] = Folder(os.path.join(path, item), self.uri.append(item), sync)
                elif os.path.isfile(os.path.join(path, item)):
                    self.items[item] = File(os.path.join(path, item), self.uri.append(item), sync)
            except Exception as e:
                logger.error(str(uri.append(item)) + ': ' + str(e))

    def matches(self, folder):
        '''
        Quickly checks recursive if the Folders are matching.
        '''
        try:
            for key in self.items.keys():
                if not self.items[key].matches(folder.items[key]):
                    return False
                return True
        except (KeyError, AttributeError):
            return False

    def sync(self, folder):
        syncList = []
        for key in self.items.keys():
            try:
                syncList += self.items[key].sync(folder.items[key])
            except KeyError:
                #localPath = self.items[key].getPath()
                #remotePath = os.path.join(folder.getPath(), (os.path.relpath(self.items[key].getPath(), self.path)))
                syncList.append((str(self.items[key].uri), str(folder.uri)))

        return syncList

    def hasHash(self):
        for key in self.items.keys():
            if not self.items[key].hasHash():
                return False
            return True


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
