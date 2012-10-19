#!/usr/bin/env python
# -*- coding: ascii -*-

"""
Wolpertinger lib for syncing

"""

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.0.1' #Versioning: http://www.python.org/dev/peps/pep-0386/

import os
import logging
import WTFile


class SyncNode(object):
	
	def __init__(self, path):
		self.path = path
		fileList = WTFile.getDir(path)
		self.pathDict = dict()
		for f in fileList:
			logging.debug('Adding file ' + os.path.relpath(f.path,path))
			self.pathDict[os.path.relpath(f.path,path)] = f
		self.hashDict = dict()
		for f in fileList:
			logging.debug('Adding file ' + os.path.relpath(f.path,path))
			self.hashDict[f.hash] = f
		
	def pathSync(self, patner):
		if(not type(patner) == type(self)):
			raise TypeError('patner must be of Type' + type(self))
		for key in list(self.pathDict):
			try:
				if(not patner.pathDict[key].path == self.pathDict[key].hash):
					logging.info('File found but is diffrent')
			except KeyError:
				logging.info('Syncing ' + self.pathDict[key].path + ' to ' + os.path.join(patner.path, key))
	
	def hashSync(self, patner):	
		if(not type(patner) == type(self)):
			raise TypeError('patner must be of Type' + type(self))
		for key in list(self.hashDict):
			try:
				if(not os.path.relpath(patner.hashDict[key].path, patner.path) == os.path.relpath(self.hashDict[key].path, self.path)):
					logging.info('File found in different location')
			except KeyError:
				logging.info('Syncing ' + self.hashDict[key].path + ' to ' + os.path.join(patner.path, os.path.relpath(self.hashDict[key].path)))
	
"""
	Tests the sync function
"""
		
def test():
	logging.basicConfig(level=logging.DEBUG)
	node1 = SyncNode('/home/konsti/Videos')
	node2 = SyncNode('/home/konsti/tmp')
	#node1.pathSync(node2)
	node1.hashSync(node2)
	pass
	
if __name__=='__main__':
    test()
