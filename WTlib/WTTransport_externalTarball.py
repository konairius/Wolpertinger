#!/usr/bin/env python
# -*- coding: ascii -*-

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.0.1'

import shutil
import logging
import concurrent.futures
import tarfile
from WTlib import WTQueue
from WTlib import WTTransport

logger = logging.getLogger(__name__)


class tarProvider(WTTransport.TransportProvider):

    def __init__(self):
        self.jobs = WTQueue.Queue()
        self.workers = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    def add(self, transportJob, priority=10):
        if transportJob.localURI == 'localhost' and transportJob.remoteURI == 'tar':
            self.jobs.put(transportJob, priority)
            self.workers.submit(self.start)
        return

    def remove(self, transportJob):
        """Removes a transport job to the providers queue"""
        return

    def start(self, transportJob=0):
        """
        Starts the first job in the providers Queue
        or if given a specific job, removes that job from the queue
        on start
        """
        return

    def getJobs(self):
        """
        Returns the currently running and enqueued
        Jobs for this Transportprovider
        """
        return

    def block(self):
        """
        Blocks till all jobs are compleated
        """
