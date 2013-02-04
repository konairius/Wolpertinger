'''
Created on Jan 24, 2013

@author: konsti
'''
import logging

FORMAT = "%(asctime)s | %(levelname)s | %(name)s: %(message)s"
logging.basicConfig(level=logging.DEBUG, filename='/home/konsti/tmp/WTBase.log', format=FORMAT)

logger = logging.getLogger(__name__)

import unittest
import Pyro4

from Util.Config import config
from Util.Uri import Uri
from Filesystem import Filesystem
from Comunication.Client import UriNotFoundError
from Comunication.Client import client as masterClient
from Comunication.Pyro import Client as PyroClient


class TestConfig(unittest.TestCase):

    def testGetExposedFolders(self):
        config().exposedFolders


class TestFilesystemFilesystem(unittest.TestCase):

    def testFile(self):
        file1 = Filesystem.File('/home/konsti/Videos/Asterix/Asterix_bei_den_Briten.mkv', Uri('WT://Testexport1.Testservice/'))
        file2 = Filesystem.File('/home/konsti/tmp/WTCache', Uri('WT://Testexport2.Testservice/'))
        self.assertTrue(file1.matches(file1), 'File dosn`t match itself...')
        self.assertFalse(file1.matches(file2), 'These files should not Match')

    def testFolder(self):
        folder1 = Filesystem.Folder('/home/konsti/Pictures', Uri('WT://Testexport1.Testservice/'))
        folder2 = Filesystem.Folder('/home/konsti/Videos', Uri('WT://Testexport2.Testservice/'))
        #  self.assertTrue(folder1.matches(folder1), 'Folder dosn`t match itself...')
        #  self.assertFalse(folder1.matches(folder2), 'These Folders should not Match')
        syncList = folder1.sync(folder2)
        for syncItem in syncList:
            logger.debug(syncItem[0] + ' -> ' + syncItem[1])


class TestUtilUri(unittest.TestCase):

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


class TestComunicationClient(unittest.TestCase):

    def testRegister(self):
        self.assertRaises(Pyro4.errors.NamingError, PyroClient)

    def testGet(self):
        uri = 'WT://export.noExeistent.Fluttershy/'
        self.assertRaises(UriNotFoundError, masterClient().get, (uri))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testWTFilesystem']
    unittest.main()
