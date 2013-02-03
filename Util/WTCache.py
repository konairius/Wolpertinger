'''
Created on Feb 3, 2013

@author: konsti
'''

import shelve
from threading import Thread
from queue import Queue


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
        self.writeQueue = Queue()
        self.writerWorker = Thread(target=self.writerWorker)
        self.writerWorker.daemon = True
        self.writerWorker.start()

    def add(self, item):
        self.writeQueue.put(item)

    def get(self, item):
        cache = shelve.open(self.cachePath, writeback=False)
        key = self.getKey(item)
        item = cache[key]
        cache.close()
        return item

    def writerWorker(self):
        while True:
            item = self.writeQueue.get(block=True)
            self.write(item)
            self.writeQueue.task_done()

    def write(self, item):
        '''
        Don't use this, it is for the writeWorker only!
        '''
        cache = shelve.open(self.cachePath, writeback=False)
        key = self.getKey(item)
        cache[key] = item
        cache.close()

    @staticmethod
    def getKey(item):
        return repr(item.__class__) + ':' + repr(item)
