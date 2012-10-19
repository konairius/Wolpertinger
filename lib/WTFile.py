#!/usr/bin/env python
# -*- coding: ascii -*-

"""
Wolpertinger Filehashing lib

"""

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.0.1' #Versioning: http://www.python.org/dev/peps/pep-0386/



import os
import hashlib
import logging
import pickle
import WTSync

"""
	Contains all relevnat File data
"""
class WTFile(object):
	
	
	def __init__(self, path):
	
		self.path = path
		self.lastChange = os.path.getmtime(path)
		self.createHash()
		
	def getHash(self):
		return self.hash
		
	def getMTime(self):
		return self.lastChange
	
	def createHash(self):
		md5 = hashlib.md5()
		with open(self.path, 'rb') as data:
			for chunk in iter(lambda: data.read(128*md5.block_size), b''):
				md5.update(chunk)
		self.hash = md5.digest()
		return self.hash
		
	def matches(self, hash):
		return self.hash == hash

"""
	Namespace Functions and Cache
"""	

def getFile(path):
	global cache
	try:
		if(os.path.getmtime(path) == cache[path].getMTime()):
			logging.debug('Cache hit for ' + path)
			return cache[path]
		else:
			logging.debug('Cached Hash for ' + path + ' is obsolete')
			del cache[path]
			return getFile(path)
	except KeyError:
		logging.debug('Creating new Hash for ' + path)
		cache[path] = WTFile(path)
		save()#Probably not the best way...
		return getFile(path)
	except NameError:
		load()
		return getFile(path)

def getDir(path):
	WTFiles = []
	for root, dirs, files in os.walk(path):
		for name in files:
			logging.debug('Scanning file ' + os.path.join(root, name))
			WTFiles.append(getFile(os.path.join(root, name)))
			
	return WTFiles
	
"""
	Persistent Hashcash
"""
def save():
	logging.info('Saving ' + str(len(cache)) + ' Hashes')
	with open('hashcache.pickle', 'wb') as hashcache:
		pickle.dump(cache, hashcache, pickle.HIGHEST_PROTOCOL)

def load():
	global cache
	try:
		with open('hashcache.pickle', 'rb') as hashcache:
			cache = pickle.load(hashcache)
	except IOError:
		cache = dict()
		
	logging.info('Loaded ' + str(len(cache)) + ' Hashes')
    	
"""
	Tests the hashing function against the /usr/src directory
"""
		
def test():
	logging.basicConfig(level=logging.DEBUG)
	hashes = getDir('/home/konsti/Videos')
	save()
	pass
	
if __name__=='__main__':
    test()
