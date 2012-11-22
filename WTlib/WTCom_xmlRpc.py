#!/usr/bin/env python
# -*- coding: ascii -*-

"""
Wolpertinger Unittest

"""

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.1.1'

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import os

from WTlib import WTFolder
from WTlib import WTConnection

import logging

logger = logging.getLogger(__name__)


class xmlRpcServer(object):

    def __init__(self):
        port = 8000
        address = 'localhost'
        server = SimpleXMLRPCServer((address, port))
        logger.info('XML-RPC open on ' + address + ':' + str(port))
        server.register_function(self.getNode, 'getNode')
        if 0 == os.fork():
            server.serve_forever()

    def getNode(self, path):
        logger.info('Getting remote sync request for ' + path)
        return WTFolder.Folder(path)


class xmlRpcClient(WTConnection.ComProvider):

    def __init__(self):
        self.connections = []

    def add(self, connection):
        if connection.remoteURI.split(':')[0] == 'http':
            self.connections.append(connection)
            return True
        return False

    def getNode(self, path, connection):
        if connection in self.connections:
            server = ServerProxy(connection.remoteURI)
            remote = WTFolder.Folder('', True, (server.getNode(path)))
            return remote
