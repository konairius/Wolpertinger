'''
Created on Jan 25, 2013

'''

import logging
logger = logging.getLogger(__name__)

#from multiprocessing import Process
from threading import Thread
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
        #self.server.registerService(Interface, self.config.getServicename())

    def stopServer(self):
        self.server.close()

    def exposeFolders(self):
        for key in self.config.getExposedFolders().keys():
            self.server.registerFolder(key, self.config.getExposedFolders()[key])


class Server(object):
    '''
    Use the manager to comuinicate with this class
    '''

    def __init__(self, address='localhost', sharedKey=None):
        '''
        should only be called by the manager
        '''
        self.config = WTConfig.getConfig()
        Pyro4.config.HMAC_KEY = sharedKey
        Pyro4.config.HOST = address
        self.isNameserver = False
        self.address = address
        self.services = []

    def close(self):
        logger.info('Closing server on ' + self.address)
        for uri, thread in self.services:
            #self.nameserver.unregister(uri)
            pass
        if self.isNameserver:
            del(self.nameserverThread)

    def enshureNameserver(self, recuresionDepth=0):
        if recuresionDepth >= 10:
            raise Pyro4.errors.NamingError
        try:
            logger.debug('Trying to locate Nameserver')
            self.nameserver = Pyro4.naming.locateNS()
            return True
        except Pyro4.errors.NamingError:
            logger.debug('Failed, starting my own one')
            self.nameserverThread = Thread(target=self.startNameserver, args=(self.address,))
            self.nameserverThread.daemon = True
            self.nameserverThread.name = 'pyronameserver'
            self.nameserverThread.start()
            self.isNameserver = True
            #time.sleep(5)
            return self.enshureNameserver(recuresionDepth+1)

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
            serveruri = pyrodaemon.register(service)
            self.nameserver.register(servicename, serveruri)
            serviceHandler = Thread(target=pyrodaemon.requestLoop)
            serviceHandler.daemon = True
            serviceHandler.name = 'pyroserver: ' + servicename
            serviceHandler.start()
            self.services.append((serveruri, serviceHandler))
        else:
            raise Pyro4.errors.NamingError()

    def registerFolder(self, folderName, path):
        if path not in self.config.getExposedFolders().values():
            raise WTFilesystem.TargetNotExposedError()
        return self.registerService(Interface(path), 'export.' + folderName + '.' + self.config.getServicename())


class Interface(object):
    '''
    The interface that will be exposed via Pyro
    '''
    def __init__(self, path):
        self.path = path
        logger.info('Creating remote interface for: ' + self.path)
        self.refresh()

    def refresh(self):
        logger.info('Updating cache for: ' + self.path)
        self.folder = WTFilesystem.Folder(self.path)

    def getFolder(self):
        logger.info('Serving remote request for: ' + self.path)
        return self.folder


class Client(object):

    def __init__(self):
        self.config = WTConfig.getConfig()
        Pyro4.config.HMAC_KEY = self.config.getSharedKey()
        self.nameserver = Pyro4.naming.locateNS()

    def findExports(self):
        logger.debug('Updating known Exports')
        self.knownExports = dict()
        exports = self.nameserver.list(prefix='export')
        for key in exports.keys():
            self.knownExports[key] = Pyro4.Proxy('PYRONAME:' + key)
        return self.knownExports.keys()

    def getFolder(self, export):
        logger.info('Requesting folder from Remote:' + export)
        if export not in self.knownExports.keys():
            self.findExports()
        try:
            return self.knownExports[export].getFolder()
        except KeyError as e:
            raise ExportNotFoundError(e)


class ExportNotFoundError(Exception):
    pass
