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

import WTFile
import WTSync


#logging.basicConfig(level=logging.INFO)

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
		
	
if __name__ == '__main__':
	unittest.main()
