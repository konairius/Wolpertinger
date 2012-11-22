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
import logging
#from concurrent.futures import ProcessPoolExecutor

from WTlib import WTFile
#from WTlib import WTConfig


logger = logging.getLogger(__name__)

#workers = ProcessPoolExecutor(max_workers=WTConfig.creationWorkers)


class Folder(object):

    def __init__(self, path='', fromDict=False, dictionary=''):
        if fromDict:
            self.__dict__.update(dictionary)
            return
        self.path = path
        elements = os.listdir(path)
        self.childs = dict()
        for element in elements:
            absolutPath = os.path.join(path, element)
            if os.path.isfile(absolutPath):
                self.childs[element] = WTFile.File(absolutPath)
            elif os.path.isdir(absolutPath):
                self.childs[element] = Folder(absolutPath)
            else:
                logger.debug('Did not know what to do with:\n' +
                            absolutPath)

    def sync(self, remote, connection, single=False):
        if not single and type(self) != type(remote):
            raise TypeError('Remote must be of type: ' + str(type(self)))
        for key in self.childs:
            if single:
                remotePath = os.path.join(remote, key)
            else:
                try:
                    self.childs[key].sync(remote=remote.childs[key],
                                          connection=connection)
                    continue
                except KeyError:
                    remotePath = os.path.join(remote.path, key)
                    logger.debug('Remote Object missing for ' +
                                 remotePath + ': Entering single Mode')
            self.childs[key].sync(remote=remotePath, connection=connection,
                                   single=True)

    def serialize(self):
        result = ''
        