#!/usr/bin/env python
# -*- coding: ascii -*-

"""
Wolpertinger DataTransport

"""

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.0.1' #Versioning: http://www.python.org/dev/peps/pep-0386/

class TransportExeption(Exeption):
	pass

class Transport(object):
	
	def __init__(self, sourcePath, targetPath, connection):
		self.sourcePath = sourcePath
		self.targetPath = targetPath
		
		for medium in connection.supportedTransports:
			if medium in connection.remote.supportedTransports:
				self.medium = medium
				break
		raise TransportExeption('No suitable Transport Found')
		
class RsyncViaSSH(Transport):
	
	
