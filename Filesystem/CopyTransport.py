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
        _copyAgent = CopyAgent
        return _copyAgent


class CopyAgent(object):
    '''
    classdocs
    '''

    def __init__(self, transportDir, workerThreads=4):
        '''
        Constructor
        '''
        self.transportDir = transportDir
        self.copyQueue = Queue()
        self.threadPool = dict()
        for num in range(workerThreads):
            self.threadPool[num] = Thread(target=self.worker)
            self.threadPool[num].daemon = True
            self.threadPool[num].start()

        logger.info('Transport Agent Running')

    def sync(self, source, target, block=False):
        if not source.isLocal():
            raise SourceNotLocalError

        self.sourceRoot = self.client.getFolder(source)
        self.targetRoot = self.client.getFolder(target)
        rawList = self.sourceRoot.sync(self.targetRoot)
        for job in rawList:
            self.copyQueue.put(job)

        if block:
            self.copyQueue.join()

    def worker(self):
        while True:
            item = self.copyQueue.get(block=True)
            virtualSource = item[0]
            virtualTarget = item[1]

            realSource = self.client.getFolder(virtualSource).path
            realTarget = self.client.getFolder(virtualTarget).path
            transportPath = path.join(self.transportDir, path.relpath(realTarget, self.targetRoot.path))

            if path.isdir(realSource):
                transportPath = path.join(transportPath, path.basename(realSource))
                logger.debug(realSource + ' => ' + transportPath)
                shutil.copytree(realSource, transportPath)
            elif path.isfile(realSource):
                logger.debug(realSource + ' => ' + transportPath)
                shutil.copy(realSource, transportPath)

            self.copyQueue.task_done()


class SourceNotLocalError(Exception):
    pass
