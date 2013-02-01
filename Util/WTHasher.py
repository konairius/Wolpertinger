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
import time


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
        for i in range(self.config.getWorkerThreads()):
            self.hashWorker = Thread(target=self.createHashWorker)
            self.hashWorker.daemon = True
            self.hashWorker.name = 'Hash Worker #' + str(i)
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
        except (KeyError, FileChangedError):
            cache.close()
            if False == sync:
                self.toHash.put(file)
                return file
            else:
                file = self.createHash(file)
                cache = shelve.open(self.config.getFileCache())
                cache[file.path] = file
                cache.close()
                return file

    def createHashWorker(self):
        while True:
            file = self.toHash.get(block=True)
            try:
                file = self.createHash(file)
            except IOError as e:
                self.toHash.put(file)
                logger.error(file.path + ': ' + str(e))
                time.sleep(10)
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
        return file


class FileChangedError(Exception):
    pass
