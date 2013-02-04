'''
Created on Jan 30, 2013

@author: konsti
'''

import logging
logger = logging.getLogger(__name__)


import hashlib
from threading import Thread
from queue import Queue
import time


from Util.WTConfig import config
from Util.WTCache import cache
from Util.WTCache import NotInCacheError


def hasher():
    global _hasher
    try:
        return _hasher
    except NameError:
        _hasher = Hasher()
        return _hasher


class Hasher(object):
    '''
    Returns the Hash of a file,
    uses Cache when possible.
    '''

    def __init__(self):
        '''
        There must only be one Hasher at Time.
        '''
        self.toHash = Queue()
        for i in range(config().workerThreads):
            self.hashWorker = Thread(target=self.createHashWorker)
            self.hashWorker.daemon = True
            self.hashWorker.name = 'Hash Worker #' + str(i)
            self.hashWorker.start()

    def hashFile(self, file, sync=False):
        try:
            cachedFile = cache().get(file)
            if cachedFile.mtime == file.mtime and cachedFile.size == file.size:
                return cachedFile
            else:
                raise FileChangedError()
        except (NotInCacheError, FileChangedError):
            if False == sync:
                self.toHash.put(file)
                return file
            else:
                file = self.createHash(file)
                cache().add(file)
                return file

    def createHashWorker(self):
        while True:
            file = self.toHash.get(block=True)
            try:
                cache().get(file)
            except NotInCacheError:
                try:
                    file = self.createHash(file)
                    cache().add(file)
                except IOError as e:
                    self.toHash.put(file)
                    logger.error(file.path + ': ' + str(e))
                    time.sleep(10)
            finally:
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


class NotYetCreatedError(Exception):
    pass
