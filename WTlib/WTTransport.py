#!/usr/bin/env python
# -*- coding: ascii -*-

"""
Wolpertinger Unittest

"""

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.1.1'

import abc
import logging
#import inspect

from WTlib import WTJobs


logger = logging.getLogger(__name__)

transportProviders = []

runningTransports = []

enqueuedTransports = []


class InvalidProviderError(Exception):
    pass


class NoTransportFoundError(Exception):
    pass


class TransportProvider(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def __init__(self):
        """Create an Instance of the Provider"""
        return

    def add(self, transportJob):
        """Adds a transport job to the providers queue,
        returns True on Success or False"""
        return

    def remove(self, transportJob):
        """Removes a transport job to the providers queue"""
        return

    def start(self, transportJob=0):
        """
        Starts the first job in the providers Queue
        or if given a specific job, removes that job from the queue
        on start
        """
        return


class tansportJob(object):

    def __init__(self, localURI, localPath, remoteURI, remotePath):
        logger.debug('New Transport Job: ' + localURI + ':' + localPath +
                     ' -> ' + remoteURI + ':' + remotePath)
        self.localURI = localURI
        self.localPath = localPath
        self.remoteURI = remoteURI
        self.remotePath = remotePath
        for provider in transportProviders:
            if provider.add(self):
                self.provider = provider
                return

        raise NoTransportFoundError('No Transportprovider for ' +
                                    remoteURI + ' was Found')

    def start(self):
        enqueuedTransports.remove(self)
        runningTransports.append(self)
        provider = transportProviders[self.method](self)
        WTJobs.workerPool.submit(provider.start)


def register(provider):
    if not issubclass(provider, TransportProvider):
        raise InvalidProviderError('The Provider ' + provider.__name__
                                   + ' could not be registered')
    TransportProvider.register(provider)
    global transportProviders
    transportProviders.append(provider)
