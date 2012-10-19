#!/usr/bin/env python
# -*- coding: ascii -*-

"""
Wolpertinger Connection between to Clients

"""

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.0.1' #Versioning: http://www.python.org/dev/peps/pep-0386/

class Connection(object):
	
	def __init__(self, localURI, remoteURI):
		self.supportedTransports = []
		self.localURI = localURI
		self.remoteURI = remoteURI
		self.nodes = []
	
	def connect(self, remote):
		self.remote = remote
