#!/usr/bin/env python
# -*- coding: ascii -*-

"""
Wolpertinger DataTransport

"""

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.0.1' #Versioning: http://www.python.org/dev/peps/pep-0386/

import os
import tarfile
import logging

import WTConnection

logger = logging.getLogger(__name__)

class TransportExeption(Exception):
	pass

class Transport(object):
	
	def __init__(self, sourcePath, targetPath, connection):
		self.sourcePath = sourcePath
		self.targetPath = targetPath
		self.connection = connection
		self.medium = 'Invalid'
		for medium in connection.supportedTransports:
			if medium in connection.remote.supportedTransports:
				self.medium = medium
				break
		if self.medium == 'Invalid':
			raise TransportExeption('No suitable Transport Found')
		
	def start(self):
		if self.medium == 'RsyncViaSSH':
			self.sync_RsyncViaSSH() #broken ... will fail
		if self.medium == 'Tarball':
			self.sync_tar()	
	#broken
	def sync_RsyncViaSSH(self):
		cid = os.fork()
		if 0 == cid:
			source = self.sourcePath
			target = self.connection.remoteURI + ":" + self.targetPath
			args = ['-ad ' , source , target]
			os.execv('/usr/bin/rsync', args)
		else:
			os.waitpid(cid,0)
			
	def sync_tar_send(self):
		logger.info('Adding ' + self.sourcePath + ' to Tarball')
		with tarfile.open('transport.tar','a') as tar:
			tar.add(self.sourcePath)
			
	def sync_tar_recive(self):
		logger.info('Reading ' + self.sourcePath + ' from Tarball')
					with tarfile.open('transport.tar','a') as tar:
