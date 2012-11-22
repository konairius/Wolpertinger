#!/usr/bin/env python
# -*- coding: ascii -*-

"""
Wolpertinger Unittest

"""

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.1.1'

import logging
import abc

from WTlib import WTFolder

logger = logging.getLogger(__name__)

comProviders = []


class InvalidProviderError(Exception):
    pass


class ComProvider(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        return

    @abc.abstractmethod
    def add(self, connection):
        return

    @abc.abstractmethod
    def getNode(self, path, connection):
        return


class Connection(object):

    def __init__(self, localURI, remoteURI):
        self.localURI = localURI
        self.remoteURI = remoteURI
        for provider in comProviders:
            if provider.add(self):
                self.provider = provider
                break

    def sync(self, localPath, remotePath, twoWay=False):
        self.localFolder = WTFolder.Folder(localPath)
        self.remoteFolder = self.provider.getNode(remotePath, self)
        self.localFolder.sync(self.remoteFolder, self)


def register(provider):
    if not issubclass(provider, ComProvider):
        raise InvalidProviderError('The Provider ' + provider.__name__
                                   + ' could not be registered')
    else:
        logger.debug('Registering ComProvider ' + provider.__name__)
    global comProviders
    comProviders.append(provider())
