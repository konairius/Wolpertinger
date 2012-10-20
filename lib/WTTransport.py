#!/usr/bin/env python
# -*- coding: ascii -*-

"""
Wolpertinger DataTransport

"""

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.0.2' #Versioning: http://www.python.org/dev/peps/pep-0386/

import os
import shutil
import tarfile
import logging

import WTConnection
import WTJobs

logger = logging.getLogger(__name__)

def addJob(localURI, localPath, remoteURI, remotePath):
	print localPath
	if('localhost' == remoteURI == localURI):
		WTJobs.queue.put(TransportJob_LocalCopy(localPath, remotePath))
		return
	raise TransportExeption('No Valid Transport method could be found')	

class TransportExeption(Exception):
	pass

	
class TransportJob_LocalCopy(object):
	
	def __init__(self, sourcePath, targetPath):
		self.sourcePath = sourcePath
		self.targetPath = targetPath
		logger.info('Adding local transport from ' + sourcePath 
		+ ' to ' + targetPath)
	def start(self):
	
		logger.info('Starting local transport from ' + self.sourcePath 
		+ ' to ' + self.targetPath)
		
		if not os.path.exists(os.path.dirname(self.targetPath)):
			os.makedirs(os.path.dirname(self.targetPath))
		shutil.copy(self.sourcePath,self.targetPath)
				
