#!/usr/bin/env python
# -*- coding: ascii -*-

"""
Wolpertinger Unittest

"""

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.1.1'

import logging

from WTlib import WTJobs


logger = logging.getLogger(__name__)

transportProviders = dict()

queue = []


class tansportJob(object):

    def __init__(self, localURI, localPath, remoteURI, remotePath):
        logger.debug('New Transport Job: ' + localURI + ':' + localPath +
                     ' -> ' + remoteURI + ':' + remotePath)
        self.localURI = localURI
        self.localPath = localPath
        self.remoteURI = remoteURI
        self.remotePath = remotePath
        self.method = self.getMethod()

    def getMethod(self):
        if self.localURI == self.remoteURI == 'localhost':
            return 'cp'
        return 'Invalid'

    def start(self):
        provider = transportProviders[self.method](self)
        WTJobs.workerPool.submit(provider.start)
