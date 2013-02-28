'''
Created on Jan 25, 2013

'''

import logging
logger = logging.getLogger(__name__)

from threading import Thread
import select

import Pyro4

from Util.Config import config
from Util.Uri import Uri
from Filesystem.Filesystem import Export
from Comunication.Client import ClientInterface
from Comunication.Client import UriNotFoundError
from Comunication.Server import ServerInterface
from Comunication.Manager import ManagerInterface


class Server(ServerInterface):
    '''
    Implements the ServerInterface for Pyro Comm
    '''

    def __init__(self):
        '''
        should only be called by the manager
        '''
        Pyro4.config.HMAC_KEY = config().sharedKey
        Pyro4.config.HOST = config().publicAddress
        self.isNameserver = False
        self.address = config().publicAddress
        self.services = []
        self.enshureNameserver()
        self.registerService(Manager(), 'manager.' + config().servicename)
        logger.info('Pyro-Server ready!')

    def close(self):
        logger.info('Closing server on ' + self.address)
        self.nameserver.remove(regex='.*\.' + config().servicename)
        self.nameserver.remove('manager.' + config().servicename)
        if self.isNameserver:
            del(self.nameserverThread)

    def enshureNameserver(self, recuresionDepth=0):
        if recuresionDepth >= 10:
            raise Pyro4.errors.NamingError()
        try:
            logger.debug('Trying to locate Nameserver')
            self.nameserver = Pyro4.naming.locateNS()
            logger.debug('Found Nameserver on ' + str(self.nameserver._pyroUri))
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
        while not config().stopEvent.is_set():
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

    def add(self, path, name):
        interface = ExportInterface(path, name)
        self.registerService(interface, interface.exportName)
        return


class ExportInterface(object):
    '''
    The interface that will be exposed via Pyro
    '''
    def __init__(self, path, name):

        self.exportName = 'export.' + name + '.' + config().servicename
        logger.info('Creating remote interface for: ' + path)
        self.export = Export(path, self.exportName)
        logger.info('Remote Interface for: ' + path + ' will be exposed on ' + str(self.export.getRootUri()))

    def refresh(self):
        self.export.refresh()

    def getItem(self, uri=None):
        if None == uri:
            uri = self.export.getRootUri()
        return self.export.getItem(uri)


class Manager(ManagerInterface):
    '''
    Interface controling the Server
    '''
    def __init__(self):
        pass

    #def sync(self, source, target):
    #    ManagerInterface.sync(source, target)


class Client(ClientInterface):

    def __init__(self):
        Pyro4.config.HMAC_KEY = config().sharedKey
        self.nameserver = Pyro4.naming.locateNS()
        self.knownExports = dict()

    def listExports(self):
        logger.debug('Updating known Exports')
        exports = self.nameserver.list(prefix='export')
        for key in exports.keys():
            self.knownExports[key] = Pyro4.Proxy('PYRONAME:' + key)
        return list(self.knownExports.keys())

    def get(self, uri):
        if not uri.__class__ == Uri:
            uri = Uri(uri)
        logger.info('Requesting Item from Remote:' + str(uri))
        if uri.exportIdentifier not in self.knownExports.keys():
            self.listExports()
        try:
            return self.knownExports[uri.exportIdentifier].getItem(uri)
        except KeyError:
            raise UriNotFoundError(str(uri))
