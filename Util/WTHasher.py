'''
Created on Jan 30, 2013

@author: konsti
'''

import logging
logger = logging.getLogger(__name__)

import shelve
import hashlib
from threading import Thread
from queue import Queue


from WTConfig import Config


def getHasher():
    global hasher
    try:
        return hasher
    except NameError:
        return Hasher()


class Hasher(object):
    '''
    Returns the Hash of a file,
    uses Cache when possible.
    '''

    def __init__(self):
        '''
        There must only be one Hasher at Time.
        '''
        global hasher
        self.toHash = Queue()
        self.config = Config()
        self.hashWorker = Thread(target=self.createHashWorker)
        self.hashWorker.daemon = True
        self.hashWorker.name = 'Hash Worker'
        self.hashWorker.start()
        hasher = self

    def hashFile(self, file, sync=False):
        try:
            cache = shelve.open(self.config.getFileCache())
            cachedFile = cache[file.path]
            cache.close()
            if cachedFile.mtime == file.mtime and cachedFile.size == file.size:
                return cachedFile
            else:
                raise FileChangedError()
        except (KeyError, FileChangedError) as e:
            cache.close()
            if False == sync:
                self.toHash.put(file)
                return file
            else:
                return self.createHash(file)

    def createHashWorker(self):
        while True:
            file = self.toHash.get(block=True)
            file = self.createHash(file)
            cache = shelve.open(self.config.getFileCache())
            cache[file.path] = file
            cache.close()
            self.toHash.task_done()

    @staticmethod
    def createHash(file):
        logger.debug('Calculating new hash for ' + file.path)
        sha1 = hashlib.sha1()
        with open(file.path, 'rb') as data:
            for chunk in iter(lambda: data.read(128 * sha1.block_size), b''):
                sha1.update(chunk)
        file.hash = sha1.hexdigest()
        file.hasHash = True
        return file


class FileChangedError(Exception):
    pass
