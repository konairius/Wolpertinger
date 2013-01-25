'''
Created on Jan 25, 2013

'''

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
