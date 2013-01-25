'''
Created on Jan 25, 2013

'''

import logging
logger = logging.getLogger(__name__)

from multiprocessing import Process
import select

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
        self.config = WTConfig.getConfig()
        manager = Manager()
        Pyro4.config.HMAC_KEY = self.config.getSharedKey()
        Pyro4.config.HOST = self.config.getPublicAddress()
        self.enshureNameserver()
        Pyro4.Daemon.serveSimple(
                                 {
                                    manager: self.config.getServicename()
                                  },
                                 ns=True
                                 )

    def enshureNameserver(self):
        try:
            Pyro4.naming.locateNS()
            return True
        except Pyro4.errors.NamingError:
            self.ns = Process(target=self.startNameserver())
            self.ns.start()
            return self.enshureNameserver()
    @staticmethod    
    def startNameserver():
        logger.info('Starting local Nameserver')
        config = WTConfig.getConfig()
        hostname = config.getPublicAddress()
        nameserverUri, nameserverDaemon, broadcastServer = Pyro4.naming.startNS(host=hostname)
        pyrodaemon=Pyro4.core.Daemon(host=hostname)
        #serveruri=pyrodaemon.register(Manager())
        #nameserverDaemon.nameserver.register('manager.' + str(hostname), serveruri)
        while True:
            nameserverSockets = set(nameserverDaemon.sockets)
            pyroSockets = set(pyrodaemon.sockets)
            rs=[broadcastServer]  # only the broadcast server is directly usable as a select() object
            rs.extend(nameserverSockets)
            rs.extend(pyroSockets)
            rs,_,_ = select.select(rs,[],[],3)
            eventsForNameserver=[]
            eventsForDaemon=[]
            for s in rs:
                if s is broadcastServer:
                    logger.debug('Broadcast server received a request')
                    broadcastServer.processRequest()
                elif s in nameserverSockets:
                    eventsForNameserver.append(s)
                elif s in pyroSockets:
                    eventsForDaemon.append(s)
            if eventsForNameserver:
                logger.debug('Nameserver received a request')
                nameserverDaemon.events(eventsForNameserver)
            if eventsForDaemon:
                logger.debug('Daemon received a request')
                pyrodaemon.events(eventsForDaemon)
                
        

class Client(object):

    def __init__(self, remoteServername):
        config = WTConfig.getConfig()
        Pyro4.config.HMAC_KEY = config.getSharedKey()
        uri = 'PYRONAME:' + remoteServername
        self.server = Pyro4.Proxy(uri)

    def getFolder(self, path):
        logger.info('Requesting folder from Remote:' + path)
        return self.server.getFolder(path)
