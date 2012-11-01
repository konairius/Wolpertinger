#!/usr/bin/env python
# -*- coding: ascii -*-

"""
Wolpertinger Unittest

"""

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.0.1'

import os
import shutil
import logging
import concurrent.futures
from WTlib import WTQueue
from WTlib import WTTransport
from WTlib import WTConfig

logger = logging.getLogger(__name__)


class cpProvider(WTTransport.TransportProvider):

    def __init__(self):
        self.jobs = WTQueue.Queue()
        self.workers = concurrent.futures.ThreadPoolExecutor(max_workers=WTConfig.transportWorkers)

    def add(self, transportJob, priority=10):
        if transportJob.localURI == transportJob.remoteURI == 'localhost':
            logger.debug('Adding transport Job to cpProvider')
            self.jobs.put(transportJob, priority)
            self.workers.submit(self.start)
            return True
        return False

    def remove(self, transportJob):
        self.jobs.remove(transportJob)

    def start(self):

        transportJob = self.jobs.get()
        if transportJob != None:
            logger.info('Starting local Copy: '
            + transportJob.localPath + ' -> '
            + transportJob.remotePath)
            if not os.path.exists(os.path.dirname(transportJob.remotePath)):
                os.makedirs(os.path.dirname(transportJob.remotePath))
            shutil.copyfile(transportJob.localPath, transportJob.remotePath)
        self.jobs.done()

        #logger.debug('Finished local Copy: '
        #             + self.sourcePath + ' -> '
        #             + self.targetPath)
        return True

    def getJobs(self):
        return self.jobs.queue

    @staticmethod
    def register():
        WTTransport.register(cpProvider)

    def block(self):
        if self.jobs.isDone():
            return False
        while not self.jobs.isDone():
            if False:
                self.workers.submit(self.start)
        return True
