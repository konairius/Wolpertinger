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


#from WTlib import WTTransport
#from WTlib import WTTransport_cp
#from WTlib import WTTransport_externalTarball
#from WTlib import WTConnection
#from WTCom import Local
from WTCom import WolpertingerRpc


class ParserTest(unittest.TestCase):

    def test_CleartextMessage(self):
        testString = 'signature:HvEjPJcGxW2K7K5;\n\
<RemoteMethodCall>\n\
    <TargetName></TargetName>\n\
    <CallId>F5AFEC97-5839-4666-B8D3-8C108B241720</CallId>\n\
    <MethodName>testMethod1</MethodName>\n\
    <Parameters>\n\
        <object type="string">This is a string-example</object>\n\
        <object type="boolean">true</object>\n\
    </Parameters>\n\
</RemoteMethodCall>'
        parser = WolpertingerRpc.MessageParser(testString)
        self.assertEqual(parser.getFlag('signature'), 'HvEjPJcGxW2K7K5',
                         'signature was not parsed Correctly')
        self.assertTrue(testString.find(parser.xml),
                        'the XML was not extracted')
        self.assertEqual(parser.type, 'RemoteMethodCall',
                         'type was not identified Correctly')

    def test_EncryptedMessage(self):
        testString = 'signature:HvEjPJcGxW2K7K5;secure:aes;gzip:50;\
            xdzBd2ITRH5uk00xz7sdPC4n4JFDKEFlAyyyeWO4WObAux4iRMi5MoQD'
        parser = WolpertingerRpc.MessageParser(testString)
        self.assertEqual(parser.getFlag('gzip'), '50',
                         'gzip was not parsed Correctly')
        self.assertEqual(parser.getFlag('secure'), 'aes',
                         'secure was not parsed Correctly')
        self.assertEqual(parser.getFlag('signature'), 'HvEjPJcGxW2K7K5',
                         'signature was not parsed Correctly')
