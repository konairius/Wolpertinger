'''
Created on Jan 25, 2013

'''

import logging
logger = logging.getLogger(__name__)

#from multiprocessing import Process
from threading import Thread
import select

import Pyro4

import WTFilesystem
import WTConfig
import WTCopyTransport
from Util import WTUri


class Manager(object):

    def __init__(self):
        self.exportTreads = dict()
        self.config = WTConfig.getConfig()

    def startServer(self):
        self.server = Server(self.config.getPublicAddress(), self.config.getSharedKey())
        self.server.enshureNameserver()

    def stopServer(self):
        self.server.close()

    def exposeFolders(self):
        for key in self.config.getExposedFolders().keys():
            self.exportTreads[key] = Thread(target=self.server.registerFolder, args=(key, self.config.getExposedFolders()[key]))
            self.exportTreads[key].start()


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
        self.enshureNameserver()
        self.registerService(ManagementInterface(), 'manager.' + self.config.getServicename())
        logger.info('Server ready!')

    def close(self):
        logger.info('Closing server on ' + self.address)
        self.nameserver.remove(regex='.*\.' + self.config.getServicename())
        self.nameserver.remove('manager.' + self.config.getServicename())
        if self.isNameserver:
            del(self.nameserverThread)

    def enshureNameserver(self, recuresionDepth=0):
        if recuresionDepth >= 10:
            raise Pyro4.errors.NamingError()
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
            return self.enshureNameserver(recuresionDepth=recuresionDepth + 1)

    @staticmethod
    def startNameserver(hostname):
        logger.info('Starting local Nameserver on ' + hostname)
        nameserverUri, nameserverDaemon, broadcastServer = Pyro4.naming.startNS(hostname)
        logger.debug('Nameserver running on ' + str(nameserverUri))
        while True:
            nameserverSockets = set(nameserverDaemon.sockets)
            rs = [broadcastServer]  # only the broadcast server is directly usable as a select() object
            rs.extend(nameserverSockets)
            rs, _, _ = select.select(rs, [], [], 3)
            eventsForNameserver = []
            for s in rs:
                if s is broadcastServer:
                    #logger.debug('Broadcast server received a request')
                    broadcastServer.processRequest()
                elif s in nameserverSockets:
                    eventsForNameserver.append(s)
            if eventsForNameserver:
                #logger.debug('Nameserver received a request')
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

    def registerFolder(self, servicename, path):
        if path not in self.config.getExposedFolders().values():
            raise WTFilesystem.TargetNotExposedError()
        self.registerService(FolderInterface(path, servicename), 'export.' + servicename + '.' + self.config.getServicename())
        return


class FolderInterface(object):
    '''
    The interface that will be exposed via Pyro
    '''
    def __init__(self, path, exportname):

        logger.info('Creating remote interface for: ' + path)
        self.export = WTFilesystem.Export(path, exportname)
        logger.info('Remote Interface for: ' + path + ' will be exposed on ' + str(self.export.getRootUri()))

    def refresh(self):
        self.export.refresh()

    def getFolder(self, uri=None):
        if None == uri:
            uri = self.export.getRootUri()
        return self.export.getItem(uri)


class ManagementInterface(object):
    '''
    Interface controling the Server
    '''
    def __init__(self):
        self.config = WTConfig.getConfig()
        self.copyAgent = WTCopyTransport.TransportAgent(self.config.getTransportDir())

    def sync(self, source, target):
        if not source.__class__ == WTUri.Uri:
            source = WTUri.Uri(source)
        if not target.__class__ == WTUri.Uri:
            target = WTUri.Uri(target)
        self.copyAgent.sync(source, target, True)


class Client(object):

    def __init__(self):
        self.config = WTConfig.getConfig()
        Pyro4.config.HMAC_KEY = self.config.getSharedKey()
        self.nameserver = Pyro4.naming.locateNS()
        self.knownExports = dict()

    def findExports(self):
        logger.debug('Updating known Exports')
        exports = self.nameserver.list(prefix='export')
        for key in exports.keys():
            self.knownExports[key] = Pyro4.Proxy('PYRONAME:' + key)
        return list(self.knownExports.keys())

    def getFolder(self, uri):
        if not uri.__class__ == WTUri.Uri:
            uri = WTUri.Uri(uri)
        logger.info('Requesting Item from Remote:' + str(uri))
        if uri.getExportIdentifier() not in self.knownExports.keys():
            self.findExports()
        try:
            return self.knownExports[uri.getExportIdentifier()].getFolder(uri)
        except KeyError as e:
            raise ExportNotFoundError(e)


class ExportNotFoundError(Exception):
    pass
