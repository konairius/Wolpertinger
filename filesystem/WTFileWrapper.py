import os
import logging
import WTFile

class WTFileWrapper(object):

	cache = dict()
		
	@staticmethod
	def getFileHash(path):
		global cache
		try:
			if(os.path.getmtime(path) == cache[path].getMTime()):
				logging.info('Cache hit for ' + path)
				return cache[path].getHash()
			else:
				logging.info('Cached Hash for ' + path + ' is obsolete')
				del cache[path]
				return getFileHash(path)
		except KeyError:
			logging.info('Creating new Hash for ' + path)
			cache[path] = WTFile.WTFile(path)
			return WTFileWrapper.getFileHash(path)
		except NameError:
			logging.info('Creating new Hashcache')
			cache = dict()
			return WTFileWrapper.getFileHash(path)

	@staticmethod	
	def getDirHashes(path):
		hashes = []
		for root, dirs, files in os.walk(path):
			for name in files:
				logging.debug('Scanning file ' + os.path.join(root, name))
				hashes.append(WTFileWrapper.getFileHash(os.path.join(root, name)))
				
		return hashes
			
	
