import os
import hashlib

class WTFile(object):
	
	
	def __init__(self, path):
		self.path = path
		self.lastChange = os.path.getmtime(path)
		self.createHash()
		
	def getHash(self):
		return self.md5.digest()
		
	def getMTime(self):
		return self.lastChange
	
	def createHash(self):
		self.md5 = hashlib.md5()
		with open(self.path, 'rb') as data:
			for chunk in iter(lambda: data.read(128*self.md5.block_size), b''):
				self.md5.update(chunk)
		return self.md5.digest()
		
	
