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
import queue

from WTlib import WTTransport

logger = logging.getLogger(__name__)


class cpProvider(WTTransport.TransportProvider):

    def __init__(self):
        self.jobs = queue.PriorityQueue()

    def add(self, transportJob, priority=10):
        if transportJob.localURI == transportJob.remoteURI == 'localhost':
            self.jobs.put(priority, transportJob)
            transportJob.priority = priority
            return True
        return False

    def remove(self, transportJob):
        self.jobs.queue.remove((transportJob.priority, transportJob))

    def start(self, transportJob=0):

        if type(transportJob) == WTTransport.tansportJob:
            self.remove(transportJob)
            self.add(transportJob, 0)
            return self.start()
        #logger.debug('Starting local Copy: '
        #             + self.sourcePath + ' -> '
        #             + self.targetPath)
        if transportJob == 0:
            transportJob = self.jobs.get()
            if not os.path.exists(os.path.dirname(transportJob[0].remotePath)):
                os.makedirs(os.path.dirname(transportJob[0].remotePath))
            shutil.copy(transportJob[0].localPath, transportJob[0].remotePath)
        #logger.debug('Finished local Copy: '
        #             + self.sourcePath + ' -> '
        #             + self.targetPath)
        #WTTransport.runningTransports.remove(self)

    def getJobs(self):
        return self.jobs.queue

    @staticmethod
    def register():
        WTTransport.register(cpProvider)
