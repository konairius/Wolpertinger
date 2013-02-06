'''
Created on Feb 4, 2013

@author: konsti
'''


import logging
from abc import ABCMeta, abstractmethod
logger = logging.getLogger(__name__)


def server():
    global _server
    try:
        return _server
    except NameError:
        _server = Server()
        return _server


class Server(object):
    '''
   The Main interface for Providing Items
    '''

    def __init__(self):
        self.knownServers = []
        self.knownExports = []

    def register(self, method):
        '''
        method must be a callable that implements ServerInterface
        '''
        newMethod = method()

        for path, name in self.knownExports:
            newMethod.add(path, name)
        self.knownServers.append(newMethod)

    def add(self, path, name):
        '''
        add the item to every registred server.
        '''
        self.knownExports.append((path, name))
        for server in self.knownServers:
            server.add(path, name)


class ServerInterface(metaclass=ABCMeta):
    '''
    The server part of a communication interface must implement this
    This server can expose a magement Interface using the Manager Class
    '''
    @abstractmethod
    def add(self, path, name):
        '''
        Adds the item to the exports and makes is accessable
        '''
        pass
