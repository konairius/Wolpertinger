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

logging.basicConfig(filename='unittest.log', level=logging.DEBUG)

from WTlib import WTFile
from WTlib import WTFolder
from WTlib import WTTransport
from WTlib import WTTransport_cp


class DefaultTest(unittest.TestCase):

    def setUp(self):
        WTTransport_cp.cpProvider.register()

    def test_createFileFromDisk(self):
        path = '/etc/hosts'
        testFile = WTFile.File(path, True)
        self.assertTrue(testFile.path == path)

    def test_createAutoCheck(self):
        path = '/etc/hosts'
        forceTestFile = WTFile.File(path, True)
        autoTestFile = WTFile.File(path, False)
        self.assertTrue(forceTestFile.path == autoTestFile.path,
                         'Paths do not match')
        self.assertTrue(forceTestFile.hash == autoTestFile.hash,
                         'Hashes do not match')
        self.assertTrue(forceTestFile.size == autoTestFile.size,
                         'Sizes do not match')
        self.assertTrue(forceTestFile.mtime == autoTestFile.mtime,
                         'Mtimes do not match')

    def test_createFolder(self):
        path = '/home/konsti/tmp/SyncTestSource'
        testFolder = WTFolder.Folder(path)
        self.assertTrue(testFolder.path == path, 'Creating failed')

    def test_localCopy(self):
        sourcePath = '/home/konsti/tmp/SyncTestSource/Episodes/tvshow.nfo'
        targetPath = '/home/konsti/tmp/SyncTestTarget/Episodes/tvshow.nfo'
        URI = 'localhost'
        transporter = WTTransport.tansportJob(URI, sourcePath,
                                              URI, targetPath)
        transporter.start()
