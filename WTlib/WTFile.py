#!/usr/bin/env python
# -*- coding: ascii -*-

"""
Wolpertinger Filehashing lib

"""

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.1.1'

import logging
import hashlib
import os

from WTlib import WTCache
from WTlib import WTTransport


class NotAFileError(Exception):
    pass


class File(object):
    def __init__(self, path, forceFromDisk=False, dummy=False):
        if dummy:
            return
        if not forceFromDisk:
            try:
                self.createFromCache(path)
                return
            except WTCache.CacheMissError:
                pass
        self.createFromDisk(path)

    def createFromDisk(self, path):
        if not os.path.isfile(path):
            raise NotAFileError('You tried to Crate a File object from\
                                something that is not a file')
        self.path = path
        self.hash = createHash(path)
        self.size = os.path.getsize(path)
        self.mtime = os.path.getmtime(path)
        cache.add(self)

    def createFromCache(self, path):
        getDict = dict()
        getDict['path'] = path
        thing = cache.get(getDict)
        self.path = thing.path
        self.hash = thing.hash
        self.size = thing.size
        self.mtime = thing.mtime
        if not (os.path.getsize(path) == self.size and
                os.path.getmtime(path) == self.mtime):
            logger.debug('Found obsolete Cache at ' + path)
            cache.remove(self)
            self.createFromDisk(path)

    def sync(self, remote, connection, single=False):
        if single:
            WTTransport.tansportJob(
                        connection.localURI,
                        self.path,
                        connection.remoteURI,
                        remote)
        else:
            if self.hash == remote.hash:
                pass
            else:
                logger.info('Conflicting file: ' + self.path)

    """
      Serialization Helper
    """
    @staticmethod
    def serializable():
        return [('path', 'TEXT'), ('hash', 'BLOB'),
                ('size', 'INTEGER'), ('mtime', 'INTEGER')]

    @staticmethod
    def deserialize(params):
        thing = File(params['path'], dummy=True)
        thing.path = params['path']
        thing.hash = params['hash']
        thing.size = params['size']
        thing.mtime = params['mtime']
        return thing

    def serialize(self):
        serialized = []
        serialized.append(self.path)
        serialized.append(self.hash)
        serialized.append(self.size)
        serialized.append(self.mtime)
        return serialized


def createHash(path):
    sha1 = hashlib.sha1()
    with open(path, 'rb') as data:
        for chunk in iter(lambda: data.read(128 * sha1.block_size), b''):
            sha1.update(chunk)
    return str(sha1.hexdigest())


cache = WTCache.Cache(File)
logger = logging.getLogger(__name__)
