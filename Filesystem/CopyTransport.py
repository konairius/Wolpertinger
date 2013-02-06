'''
Created on Jan 28, 2013

@author: konsti
'''

import logging
logger = logging.getLogger(__name__)


from queue import Queue
from os import path
import shutil
from threading import Thread


def copyAgent():
    global _copyAgent
    try:
        return _copyAgent
    except NameError:
        _copyAgent = CopyAgent()
        return _copyAgent


class CopyAgent(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.copyQueue = Queue()
        self.threadPool = dict()
        for num in range(1):
            self.threadPool[num] = Thread(target=self.worker)
            self.threadPool[num].daemon = True
            self.threadPool[num].start()

        logger.info('Transport Agent Running')

    def add(self, source, target, block=False):
        self.copyQueue.put((source, target))
        if block:
            self.copyQueue.join()

    def join(self):
        return self.copyQueue.join()

    def worker(self):
        while True:
            item = self.copyQueue.get(block=True)

            source = item[0]
            target = item[1]

            if path.isdir(source):
                target = path.join(target, path.basename(source))
                logger.debug(source + ' => ' + target)
                shutil.copytree(source, target)
            elif path.isfile(source):
                logger.debug(source + ' => ' + target)
                shutil.copy(source, target)

            self.copyQueue.task_done()


class SourceNotLocalError(Exception):
    pass
