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
from Util.WTUri import Uri


class TestWTConfig(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.config = WTConfig.getConfig()

    def testGetExposedFolders(self):
        self.config.getExposedFolders()


class TestWTFilesystem(unittest.TestCase):

    def testFile(self):
        file1 = WTFilesystem.File.fromPath('/home/konsti/tmp/WTBase.log', Uri('WT://Testexport1.Testservice/'))
        file2 = WTFilesystem.File.fromPath('/home/konsti/tmp/WTFiles', Uri('WT://Testexport2.Testservice/'))
        self.assertTrue(file1.matches(file1), 'File dosn`t match itself...')
        self.assertFalse(file1.matches(file2), 'These files should not Match')

    def testFolder(self):
        folder1 = WTFilesystem.Folder('/home/konsti/tmp', Uri('WT://Testexport1.Testservice/'))
        folder2 = WTFilesystem.Folder('/home/konsti/tmp2', Uri('WT://Testexport2.Testservice/'))
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
        #time.sleep(5)
        manager.stopServer()

    def testExposeFolders(self):
        manager = WTPyro.Manager()
        manager.startServer()
        #time.sleep(5)
        manager.exposeFolders()
        #time.sleep(5)
        manager.stopServer()


class TestWTPyroClient(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.manager = WTPyro.Manager()
        self.manager.startServer()
        self.manager.exposeFolders()
        #time.sleep(10)
        self.client = WTPyro.Client()

    def testFindExports(self):
        exports = self.client.findExports()
        for export in exports:
            logger.debug('Found export: ' + export)

    def testGetFolder(self):
        folders = dict()
        for export in self.client.findExports():
            folders[export] = self.client.getFolder(Uri.fromExportIdentifier(export))

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.manager.stopServer()


class TestUtilWTUri(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.rootUri = Uri('WT://Testexport1.Testservice/')
        self.subUri = Uri('WT://Testexport1.Testservice/something')

    def testCreateUri(self):
        self.rootUri = Uri('WT://Testexport1.Testservice/')
        self.subUri = Uri('WT://Testexport1.Testservice/something')

    def testGetExportIdentifier(self):
        self.assertEqual(self.rootUri.getExportIdentifier(), 'Testexport1.Testservice',
                          'Exportidentifier was not found correctly')

    def testGetPath(self):
        self.assertEqual(self.rootUri.getPath(), '/', 'Path was not found correctly')

    def testAppend(self):
        self.assertEqual(self.rootUri.append('something').string, self.subUri.string, 'Append did not work')

    def testContains(self):
        self.assertTrue(self.rootUri.contains(self.subUri))
        self.assertFalse(self.subUri.contains(self.rootUri))

    def testGetNextItem(self):
        self.assertEqual(self.subUri.getNextItem(self.rootUri), 'something')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testWTFilesystem']
    unittest.main()
