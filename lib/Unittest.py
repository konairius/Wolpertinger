#!/usr/bin/env python
# -*- coding: ascii -*-

"""
Wolpertinger Unittest

"""

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.0.1' #Versioning: http://www.python.org/dev/peps/pep-0386/

import unittest
import logging
import tarfile
import pickle

import WTFile
import WTSync
import WTConnection
#import WTTransport


logging.basicConfig(level=logging.INFO)

class TestWTFile(unittest.TestCase):
	
	#def setUp(self):
		
		
	def test_type(self):
		testFile = WTFile.getFile('/etc/hosts')
		self.assertTrue(type(testFile) == WTFile.WTFile)
		
	def test_massHashing(self):
		testFiles = WTFile.getDir('/home/konsti/Music')
		
		
class TestWTSync(unittest.TestCase):
	
	def setUp(self):
		self.node1 = WTSync.SyncNode('/home/konsti/Music')
		self.node2 = WTSync.SyncNode('/home/konsti/Pictures')
	
	def test_pathSync(self):
		toSync, conflicting = self.node1.pathSync(self.node2)
		for key in list(toSync):
			self.assertTrue(not key in conflicting)
		
	def test_hashSync(self):
		toSync, conflicting = self.node1.hashSync(self.node2)
		for key in list(toSync):
			self.assertTrue(not key in conflicting)
			
	def test_fullSync(self):
		toSync, conflicting, toMove = self.node1.sync(self.node2)
		for key in list(toSync):
			self.assertTrue(not key in conflicting)
			self.assertTrue(not key in toMove)

class TestWTConnection(unittest.TestCase):
	
	#def setUp(self):
		
		
	def test_createNodesLocal(self):
		con = WTConnection.Connection('localhost','localhost')
		con.addSync('/home/konsti/tmp/SyncTestSource'
				   ,'/home/konsti/tmp/SyncTestTarget')
		self.assertTrue(con.nodes[0][0].path == '/home/konsti/tmp/SyncTestSource')
		self.assertTrue(con.nodes[0][1].path == '/home/konsti/tmp/SyncTestTarget')
		con.startTransfer()
'''		
class TestWTTransport(unittest.TestCase):

	def setUp(self):
		self.local = WTConnection.Connection('localhost','fileserver')
		self.local.supportedTransports.append('RsyncViaSSH')
		
		self.remote = WTConnection.Connection('fileserver','localhost')
		self.remote.supportedTransports.append('RsyncViaSSH')
		
		self.local.connect(self.remote)
		
	def test_RsyncViaSSH(self):
		transport = WTTransport.Transport('/home/konsti/Pokemon Emerald.sav', '/tmp/test2', self.local)
		transport.start()
'''
'''		
class TestWTAll(unittest.TestCase):
	def setUp(self):
		self.local = WTConnection.Connection('localhost','localhost')
		self.local.supportedTransports.append('Tarball')
		
		self.remote = WTConnection.Connection('localhost','localhost')
		self.remote.supportedTransports.append('Tarball')
		
		self.local.connect(self.remote)
		
		self.local.nodes.append(WTSync.SyncNode('/home/konsti/Music'))
		self.remote.nodes.append(WTSync.SyncNode('/tmp'))
		
	def test_sync(self):
		toSync, conflicting, toMove = self.local.nodes[0].sync(self.local.remote.nodes[0])
		for key in list(toSync):
			self.assertTrue(not key in conflicting)
			self.assertTrue(not key in toMove)
			#logger
			transport = WTTransport.Transport(toSync[key].path, key, self.local)
			transport.start()
			pickle
			with tarfile.open('transport.tar','a') as tar:
				tar.add(self.sourcePath)
'''		
		
	
if __name__ == '__main__':
	unittest.main()

	#suite = unittest.TestLoader().loadTestsFromTestCase(TestWTAll)
	#unittest.TextTestRunner(verbosity=2).run(suite)
