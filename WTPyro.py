'''
Created on Jan 25, 2013

'''

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.0.1'

import logging
logger = logging.getLogger(__name__)


import Pyro4

import WTFilesystem
import WTConfig


class Manager(object):

    def __init__(self):
        pass

    def getFolder(self, path):
        logger.info('Serving remote Request: ' + path)
        return WTFilesystem.Folder(path)


class Server(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        manager = Manager()
        Pyro4.Daemon.serveSimple(
                                 {
                                    manager: WTConfig.getServername()
                                  },
                                 ns=True
                                 )


class Client(object):

    def __init__(self, remoteServername):
        uri = 'PYRONAME:' + remoteServername
        self.server = Pyro4.Proxy(uri)

    def getFolder(self, path):
        logger.info('Requesting folder from Remote:' + path)
        return self.server.getFolder(path)
