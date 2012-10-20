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

logger = logging.getLogger(__name__)

class SyncNode(object):
	
	def __init__(self, path):
		self.path = path
		fileList = WTFile.getDir(path)
		self.pathDict = dict()
		for f in fileList:
			#logger.debug('Adding file ' + os.path.relpath(f.path,path))
			self.pathDict[os.path.relpath(f.path,path)] = f
		self.hashDict = dict()
		for f in fileList:
			#logger.debug('Adding file ' + os.path.relpath(f.path,path))
			self.hashDict[f.hash] = f
	
	#TODO: Rewrite	
	def pathSync(self, patner):
		if(not type(patner) == type(self)):
			raise TypeError('patner must be of Type' + type(self))
			
		conflictingFiles = dict()
		copyFiles = dict()
		for key in list(self.pathDict):
			try:
				if(not patner.pathDict[key].hash == self.pathDict[key].hash):
					logger.debug('Conflicting File found at ' 
					+ patner.pathDict[key].path)
					conflictingFiles[patner.pathDict[key].path] = self.pathDict[key]
					
			except KeyError:
				logger.debug('By Path: Copy file from ' 
				+ self.pathDict[key].path 
				+ ' to '
				+ os.path.join(patner.path, key))
				copyFiles[os.path.join(patner.path, key)] = self.pathDict[key]
				
		return copyFiles, conflictingFiles
				 
	#TODO: Rewrite
	def hashSync(self, patner):	
		if(not type(patner) == type(self)):
			raise TypeError('patner must be of Type' + type(self))
			
		moveFiles = dict()
		copyFiles = dict()
		for key in list(self.hashDict):
			try:
				if(not os.path.relpath(patner.hashDict[key].path, patner.path) 
				== os.path.relpath(self.hashDict[key].path, self.path)):
					logger.debug('File found at ' 
					+ os.path.relpath(patner.hashDict[key].path, patner.path) 
					+ ' expected ' 
					+ os.path.relpath(self.hashDict[key].path, self.path))
					moveFiles[os.path.join(patner.path
											, os.path.relpath(
											self.hashDict[key].path
											, self.path))] = self.hashDict[key]
			except KeyError:
				logger.debug('By Hash: Copy file from ' 
				+ self.hashDict[key].path + ' to ' 
				+ os.path.join(patner.path
								, os.path.relpath(
								self.hashDict[key].path, self.path)))
				copyFiles[os.path.join(patner.path
										, os.path.relpath(
										self.hashDict[key].path
										, self.path))] = self.hashDict[key]
						  
		return copyFiles, moveFiles
	
	#TODO: Rewrite
	def sync(self, patner):
		pathCopy, conflictingFiles = self.pathSync(patner)
		hashCopy, moveFiles = self.hashSync(patner)
		copyFiles = dict()
		for key in list(pathCopy):
			try:
				if(hashCopy[key] == pathCopy[key]):
					copyFiles[key] = pathCopy[key]
				else:
					raise RuntimeError('Files that are the same are not, '+
					'check your system for memory Corruption')
			except KeyError:
				pass	
		return pathCopy, conflictingFiles, moveFiles
		
	def getTransferFiles(self, patner):
		copyFiles, conflictingFiles, moveFiles = self.sync(patner)
		files = []
		for key in list(copyFiles):
			files.append((copyFiles[key].path, key))
		return files
	
"""
	Tests the sync function
"""
		
def test():
	logging.basicConfig(level=logging.DEBUG)

	pass
	
if __name__=='__main__':
    test()
