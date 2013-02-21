'''
Created on Feb 4, 2013

@author: konsti
'''

import logging
logger = logging.getLogger(__name__)

from Util.Uri import Uri
from abc import ABCMeta, abstractmethod


def client():
    global _client
    try:
        return _client
    except NameError:
        _client = Client()
        return _client


class Client(object):
    '''
    Interface for acquiring Items
    '''

    def __init__(self):
        self.knownClients = []

    def register(self, method):
        '''
        method must be a callable that implements ClientInterface
        '''
        self.knownClients.append(method())

    def get(self, uri):
        if not uri.__class__ == Uri:
            uri = Uri(uri)
        for method in self.knownClients:
            try:
                result = method.get(uri)
                return result
            except UriNotFoundError:
                pass
        raise UriNotFoundError(str(uri))

    def listExports(self):
        exports = []
        for method in self.knownClients:
            exports += method.listExports()
        return exports


class ClientInterface(metaclass=ABCMeta):
    '''
    The client part of a communication interface must implement this
    '''
    @abstractmethod
    def get(self, uri):
        '''
        Returns the Item the Uri is pointing to or raises a UriNotFoundError
        '''
        pass

    def listExports(self):
        '''
        Return all known (or found) exports
        '''


class UriNotFoundError(Exception):
    pass
