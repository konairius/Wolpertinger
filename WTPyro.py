'''
Created on Jan 25, 2013

'''

import logging
logger = logging.getLogger(__name__)

from multiprocessing import Process
import select
import time

import Pyro4

import WTFilesystem
import WTConfig


class Manager(object):

    def __init__(self):
        self.config = WTConfig.getConfig()

    def startServer(self):
        self.server = Server(self.config.getPublicAddress())
        self.server.enshureNameserver()
        self.server.registerService(Interface, self.config.getServicename())

    def stopServer(self):
        self.server.close()


class Server(object):
    '''
    Use the manager to comuinicate with this class
    '''

    def __init__(self, address='localhost', sharedKey=None):
        '''
        should only be called by the manager
        '''
        Pyro4.config.HMAC_KEY = sharedKey
        Pyro4.config.HOST = address
        self.isNameserver = False
        self.address = address
        self.services = []

    def close(self):
        logger.info('Closing server on ' + self.address)
        for uri, process in self.services:
            self.nameserver.unregister(uri)
            process.terminate()
        if self.isNameserver:
            self.nameserverProcess.terminate()

    def enshureNameserver(self):
        try:
            logger.debug('Trying to locate Nameserver')
            self.nameserver = Pyro4.naming.locateNS()
            return True
        except Pyro4.errors.NamingError:
            logger.debug('Failed, starting my own one')
            self.nameserverProcess = Process(target=self.startNameserver, args=(self.address,))
            self.nameserverProcess.start()
            self.isNameserver = True
            time.sleep(5)
            return self.enshureNameserver()

    @staticmethod
    def startNameserver(hostname):
        logger.info('Starting local Nameserver on ' + hostname)
        nameserverUri, nameserverDaemon, broadcastServer = Pyro4.naming.startNS(hostname)
        while True:
            nameserverSockets = set(nameserverDaemon.sockets)
            rs = [broadcastServer]  # only the broadcast server is directly usable as a select() object
            rs.extend(nameserverSockets)
            rs, _, _ = select.select(rs, [], [], 3)
            eventsForNameserver = []
            for s in rs:
                if s is broadcastServer:
                    logger.debug('Broadcast server received a request')
                    broadcastServer.processRequest()
                elif s in nameserverSockets:
                    eventsForNameserver.append(s)
            if eventsForNameserver:
                logger.debug('Nameserver received a request')
                nameserverDaemon.events(eventsForNameserver)

    def registerService(self, service, servicename):
        if self.enshureNameserver():
            pyrodaemon = Pyro4.core.Daemon(host=self.address)
            serveruri = pyrodaemon.register(service())
            self.nameserver.register(servicename, serveruri)
            serviceHandler = Process(target=pyrodaemon.requestLoop)
            serviceHandler.start()
            self.services.append((serveruri, serviceHandler))
        else:
            raise Pyro4.errors.NamingError()


class Client(object):

    def __init__(self, remoteServername):
        config = WTConfig.getConfig()
        Pyro4.config.HMAC_KEY = config.getSharedKey()
        uri = 'PYRONAME:' + remoteServername
        self.server = Pyro4.Proxy(uri)

    def getFolder(self, path):
        logger.info('Requesting folder from Remote:' + path)
        return self.server.getFolder(path)


class Interface(object):
    '''
    The interface that will be exposed via Pyro
    '''
    def __init__(self):
        pass

    def getFolder(self, path):
        logger.info('Serving remote Request: ' + path)
        return WTFilesystem.Folder(path)
