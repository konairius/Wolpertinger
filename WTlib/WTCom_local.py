#!/usr/bin/env python
# -*- coding: ascii -*-

"""
Wolpertinger Unittest

"""

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.1.1'

from WTlib import WTFolder
from WTlib import WTConnection
import logging

logger = logging.getLogger(__name__)


class localCom(WTConnection.ComProvider):

    def __init__(self):
        self.connections = []

    def add(self, connection):
        if connection.remoteURI == connection.localURI == 'localhost':
            self.connections.append(connection)
            return True
        return False

    def getNode(self, path, connection):
        return WTFolder.Folder(path)
