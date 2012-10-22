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

from WTlib import WTFile


logger = logging.getLogger(__name__)


class Folder(object):

    def __init__(self, path):
        self.path = path
        elements = os.listdir(path)
        self.childs = dict()
        for element in elements:
            element = os.path.join(path, element)
            if os.path.isfile(element):
                self.childs[element] = WTFile.File(element)
            elif os.path.isdir(element):
                self.childs[element] = Folder(element)
            else:
                logger.debug(element)
                logger.debug(os.stat(element))

    def sync(self, remote):
        if type(self) != type(remote):
            raise TypeError('Remote must be of type: ' + str(type(self)))
