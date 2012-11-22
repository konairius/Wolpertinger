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
from WTlib import WTTransport_externalTarball
from WTlib import WTConnection
from WTlib import WTCom_local
from WTlib import WTCom_WolpertingerRpc


class LocalTest(unittest.TestCase):

    def setUp(self):
        if len(WTTransport.transportProviders) == 0:
            WTTransport.register(WTTransport_cp.cpProvider)
            WTTransport.register(WTTransport_externalTarball.tarProvider)
            WTConnection.register(WTCom_local.localCom)

    def test_LocalSync(self):
        URI = 'localhost'
        sourcePath = '/home/konsti/tmp/SyncTestSource'
        targetPath = '/home/konsti/tmp/SyncTestTarget'
        connection = WTConnection.Connection(URI, URI)
        connection.sync(sourcePath, targetPath)
        WTTransport.block()

    def test_TarSync(self):
        localURI = 'localhost'
        remoteURI = 'tar:localhost'
        sourcePath = '/home/konsti/tmp/SyncTestSource'
        targetPath = '/home/konsti/tmp/SyncTestTarget'
        connection = WTConnection.Connection(localURI, remoteURI)
        connection.sync(sourcePath, targetPath)
        WTTransport.block()

    def test_wolpertingerRpcParser(self):
        testString = 'signature:HvEjPJcGxW2K7K5;secure:aes;gzip:50;\
            xdzBd2ITRH5uk00xz7sdPC4n4JFDKEFlAyyyeWO4WObAux4iRMi5MoQD'
        parser = WTCom_WolpertingerRpc.MessageParser(testString)
        self.assertEqual(parser.getFlag('gizp'), '50',
                         'gzip was not parsed Correctly')
        self.assertEqual(parser.getFlag('secure'), 'aes',
                         'secure was not parsed Correctly')
        self.assertEqual(parser.getFlag('signature'), 'HvEjPJcGxW2K7K5',
                         'signature was not parsed Correctly')
