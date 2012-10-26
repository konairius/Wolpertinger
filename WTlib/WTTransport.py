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


logger = logging.getLogger(__name__)

transportProviders = []


class InvalidProviderError(Exception):
    pass


class NoTransportFoundError(Exception):
    pass


class TransportProvider(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self):
        """Create an Instance of the Provider"""
        return

    @abc.abstractmethod
    def add(self, transportJob, priority=10):
        """Adds a transport job to the providers queue,
        returns True on Success or False"""
        return

    @abc.abstractmethod
    def remove(self, transportJob):
        """Removes a transport job to the providers queue"""
        return

    @abc.abstractmethod
    def start(self, transportJob=0):
        """
        Starts the first job in the providers Queue
        or if given a specific job, removes that job from the queue
        on start
        """
        return

    @abc.abstractmethod
    def getJobs(self):
        """
        Returns the currently running and enqueued
        Jobs for this Transportprovider
        """
        return


class tansportJob(object):

    def __init__(self, localURI, localPath, remoteURI, remotePath):

        self.localURI = localURI
        self.localPath = localPath
        self.remoteURI = remoteURI
        self.remotePath = remotePath
        for provider in transportProviders:
            if provider.add(self):
                self.provider = provider
                logger.debug('New Transport Job: ' + localURI + ':'
                             + localPath +
                             ' -> ' + remoteURI + ':' + remotePath)
                return

        raise NoTransportFoundError('No Transportprovider for ' +
                                    remoteURI + ' was Found')

    #def start(self):
    #    self.provider.start(self)


def register(provider):
    if not issubclass(provider, TransportProvider):
        raise InvalidProviderError('The Provider ' + provider.__name__
                                   + ' could not be registered')
    #TransportProvider.register(provider)
    global transportProviders
    transportProviders.append(provider())
