'''
Created on Jan 24, 2013

@author: konsti
'''
import logging

FORMAT = "%(asctime)s | %(levelname)s | %(name)s: %(message)s"
logging.basicConfig(level=logging.DEBUG, filename='/home/konsti/tmp/WTBase.log', format=FORMAT)

logger = logging.getLogger(__name__)

import time
import unittest
from multiprocessing import Process

import WTFilesystem
import WTPyro
import WTConfig


class TestWTConfig(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.config = WTConfig.getConfig()

    def testGetExposedFolders(self):
        self.config.getExposedFolders()


class TestWTFilesystem(unittest.TestCase):

    def testFile(self):
        file1 = WTFilesystem.File.fromPath('/home/konsti/tmp/WTBase.log')
        file2 = WTFilesystem.File.fromPath('/home/konsti/tmp/WTFiles')
        self.assertTrue(file1.matches(file1), 'File dosn`t match itself...')
        self.assertFalse(file1.matches(file2), 'These files should not Match')

    def testFolder(self):
        folder1 = WTFilesystem.Folder('/home/konsti/tmp')
        folder2 = WTFilesystem.Folder('/home/konsti/tmp2')
        #  self.assertTrue(folder1.matches(folder1), 'Folder dosn`t match itself...')
        #  self.assertFalse(folder1.matches(folder2), 'These Folders should not Match')
        syncList = folder1.sync(folder2, True)
        for syncItem in syncList:
            logger.debug(syncItem[0] + ' -> ' + syncItem[1])

        logger.debug('Created ' + str(WTFilesystem.fileCounter) + ' File Objects!')


class TestWTPyroManager(unittest.TestCase):

    def testManager(self):
        manager = WTPyro.Manager()
        manager.startServer()
        time.sleep(5)
        manager.stopServer()


class TestWTPyroClient(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.manager = WTPyro.Manager()
        self.manager.startServer()
        time.sleep(5)

    def testClient(self):
        folder1 = WTFilesystem.Folder('/home/konsti/tmp')
        client = WTPyro.Client('WTTest')
        folder2 = client.getFolder('/home/konsti/tmp2')
        syncList = folder1.sync(folder2, True)
        for syncItem in syncList:
            logger.debug(syncItem[0] + ' -> ' + syncItem[1])

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.manager.stopServer()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testWTFilesystem']
    unittest.main()
