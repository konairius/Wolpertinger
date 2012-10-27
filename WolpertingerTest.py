#!/usr/bin/env python3
# -*- coding: ascii -*-

"""
Wolpertinger Unittest

"""

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.0.1'

import unittest
import logging

FORMAT = "%(asctime)s | %(levelname)s | %(name)s: %(message)s"

logging.basicConfig(format=FORMAT,
                    filename='unittest.log',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


from WTlib import WTTransport
from WTlib import WTTransport_cp
from WTlib import WTConnection
from WTlib import WTCom_local


class LocalTest(unittest.TestCase):

    def setUp(self):
        WTTransport.register(WTTransport_cp.cpProvider)
        WTConnection.register(WTCom_local.localCom)

    def test_LocalSync(self):
        URI = 'localhost'
        sourcePath = '/home/konsti/tmp/SyncTestSource'
        targetPath = '/home/konsti/tmp/SyncTestTarget'
        connection = WTConnection.Connection(URI, URI)
        connection.sync(sourcePath, targetPath)
        WTTransport.block()
