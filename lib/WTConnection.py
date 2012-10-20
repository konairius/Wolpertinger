#!/usr/bin/env python
# -*- coding: ascii -*-

"""
Wolpertinger Connection between to Clients

"""

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.0.2' #Versioning: http://www.python.org/dev/peps/pep-0386/

import shutil

import WTSync

def getRemoteNode(remoteURI, remotePath, localURI):
	if 'localhost' == remoteURI:
		return WTSync.SyncNode(remotePath)
	raise NotImplementedError('No valid Communication Protocol found')

def getTransferMethod(remoteURI, localURI):
	if 'localhost' == remoteURI:
		return 'cp'
	raise NotImplementedError('No valid Transfer Protocol found')

class Connection(object):
	
	def __init__(self, localURI, remoteURI):
		self.localURI = localURI
		self.remoteURI = remoteURI
		self.nodes = []
		
	def addSync(self, localPath, remotePath):
		localNode = WTSync.SyncNode(localPath)
		remoteNode = getRemoteNode(self.remoteURI,remotePath,self.localURI)
		self.nodes.append((localNode,remoteNode))
		
	def startTransfer(self, nodesId = -1, twoway = False):
		method = getTransferMethod(self.remoteURI, self.localURI)
		copyFiles = []
		if -1 == nodesId:
			for link in self.nodes:
		 		copyFiles.append(link[0].getTransferFiles(link[1]))
		 		if twoway:
		 			copyFiles.append(link[1].getTransferFiles(link[0]))
		else:
		 	copyFiles.append(self.nodes[nodesId][0].getTransferFiles(self.nodes[nodesId][1]))
		 	if twoway:
		 		copyFiles.append(self.nodes[nodesId][1].getTransferFiles(self.nodes[nodesId][0]))
		if 'cp' == method:
			for copyJob in copyFiles[0]:
				shutil.copy(copyJob[0],copyJob[1])
