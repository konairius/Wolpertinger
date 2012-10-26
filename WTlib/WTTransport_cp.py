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
from WTlib import WTQueue

from WTlib import WTTransport

logger = logging.getLogger(__name__)


class cpProvider(WTTransport.TransportProvider):

    def __init__(self):
        self.jobs = WTQueue.Queue()

    def add(self, transportJob, priority=10):
        if transportJob.localURI == transportJob.remoteURI == 'localhost':
            logger.debug('Adding transport Job to cpProvider')
            self.jobs.put(transportJob, priority)
            return True
        return False

    def remove(self, transportJob):
        self.jobs.remove(transportJob)

    def start(self):

        #logger.debug('Starting local Copy: '
        #             + self.sourcePath + ' -> '
        #             + self.targetPath)
        transportJob = self.jobs.get()
        if transportJob != None:
            if not os.path.exists(os.path.dirname(transportJob.remotePath)):
                os.makedirs(os.path.dirname(transportJob.remotePath))
            shutil.copy(transportJob.localPath, transportJob.remotePath)
        #logger.debug('Finished local Copy: '
        #             + self.sourcePath + ' -> '
        #             + self.targetPath)
        #WTTransport.runningTransports.remove(self)

    def getJobs(self):
        return self.jobs.queue

    @staticmethod
    def register():
        WTTransport.register(cpProvider)
