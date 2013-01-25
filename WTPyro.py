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
        config = WTConfig.getConfig()
        manager = Manager()
        Pyro4.config.HMAC_KEY = config.getSharedKey()
        Pyro4.Daemon.serveSimple(
                                 {
                                    manager: config.getServicename()
                                  },
                                 ns=True
                                 )


class Client(object):

    def __init__(self, remoteServername):
        config = WTConfig.getConfig()
        Pyro4.config.HMAC_KEY = config.getSharedKey()
        uri = 'PYRONAME:' + remoteServername
        self.server = Pyro4.Proxy(uri)

    def getFolder(self, path):
        logger.info('Requesting folder from Remote:' + path)
        return self.server.getFolder(path)
