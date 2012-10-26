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

from WTlib import WTTransport

logger = logging.getLogger(__name__)


class cpProvider(WTTransport.TransportProvider):

    def __init__(self, transportJob):
        self.sourcePath = transportJob.localPath
        self.targetPath = transportJob.remotePath

    def start(self):
        logger.debug('Starting local Copy: '
                     + self.sourcePath + ' -> '
                     + self.targetPath)
        if not os.path.exists(os.path.dirname(self.targetPath)):
            os.makedirs(os.path.dirname(self.targetPath))
        shutil.copy(self.sourcePath, self.targetPath)
        logger.debug('Finished local Copy: '
                     + self.sourcePath + ' -> '
                     + self.targetPath)
        #WTTransport.runningTransports.remove(self)

    @staticmethod
    def register():
        WTTransport.register(cpProvider)
