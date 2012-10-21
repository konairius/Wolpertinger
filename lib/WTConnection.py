#!/usr/bin/env python
# -*- coding: ascii -*-

"""
Wolpertinger Connection between to Clients

"""

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.0.2' #Versioning: http://www.python.org/dev/peps/pep-0386/

import WTSync
import WTTransport

def getRemoteNode(remoteURI, remotePath, localURI):
	if 'localhost' == remoteURI:
		return WTSync.SyncNode(remotePath)
	raise NotImplementedError('No valid Communication Protocol found')

class Connection(object):
	
	def __init__(self, localURI, remoteURI):
		self.localURI = localURI
		self.remoteURI = remoteURI
		self.nodes = []
		
	def addSync(self, localPath, remotePath):
		localNode = WTSync.SyncNode(localPath)
		remoteNode = getRemoteNode(self.remoteURI,remotePath,self.localURI)
		self.nodes.append((localNode,remoteNode))
		
	def startSync(self, nodesId = -1, twoway = False):
		copyFiles = []
		nodes = []
		print('startSync')
		if -1 == nodesId:
			nodes = self.nodes
		else:
			nodes.append(nodes[nodesId])
		print(nodes)
		for link in nodes:
	 		copyFiles += (link[0].getTransferFiles(link[1]))
	 		if twoway:
	 			copyFiles += (link[1].getTransferFiles(link[0]))
	 	for job in copyFiles:
	 		print(job)
	 		WTTransport.addJob(self.localURI, job[0], self.remoteURI, job[1])
