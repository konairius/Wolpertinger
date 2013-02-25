'''
Created on Feb 6, 2013

@author: konsti
'''

import logging
from abc import ABCMeta, abstractmethod

logger = logging.getLogger(__name__)

from Comunication.Client import client
from Filesystem.TransportAgent import agent


class Manager(object):
    '''
    The manager is the main interface for user interaction
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass

    def sync(self, source, target):
        sourceFolder = client().get(source)
        targetFolder = client().get(target)
        agent().add(sourceFolder.sync(targetFolder))


class ManagerInterface(metaclass=ABCMeta):
    '''
    The Interface the Comm method must Implemented in order to allow management
    '''
    @abstractmethod
    def sync(self, source, target):
        '''
        finds all differences between source and target
        '''
        Manager().sync(source, target)
