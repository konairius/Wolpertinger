#!/usr/bin/env python
# -*- coding: ascii -*-

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.0.1'

import os
import shutil
import logging
import concurrent.futures
import tarfile
from WTlib import WTQueue
from WTlib import WTTransport
from WTlib import WTConfig

logger = logging.getLogger(__name__)


class tarProvider(WTTransport.TransportProvider):

    def __init__(self):
        self.jobs = WTQueue.Queue()
        self.workers = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    def add(self, transportJob, priority=10):
        if transportJob.localURI == 'localhost' and transportJob.remoteURI.split(':')[0] == 'tar':
            self.jobs.put(transportJob, priority)
            self.workers.submit(self.start)
            return True
        return False

    def remove(self, transportJob):
        self.jobs.remove(transportJob)
        return

    def start(self, transportJob=0):
        transportJob = self.jobs.get()
        if transportJob != None:
            tarPath = os.path.join(WTConfig.tarTransportPath,
                                   transportJob.remoteURI + '.tar')
            logger.info('Starting Tar Transport using file' + tarPath + ': '
            + transportJob.localPath + ' -> '
            + transportJob.remotePath)
            with tarfile.open(tarPath, 'a') as tar:
                tar.add(transportJob.localPath,
                        transportJob.remotePath)
        self.jobs.done()
        return True

    def getJobs(self):
        """
        Returns the currently running and enqueued
        Jobs for this Transportprovider
        """
        return

    def block(self):
        if self.jobs.isDone():
            return False
        while not self.jobs.isDone():
            if False:
                self.workers.submit(self.start)
        return True
