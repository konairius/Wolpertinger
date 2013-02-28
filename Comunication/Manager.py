'''
Created on Feb 6, 2013

@author: konsti
'''

import logging
from abc import ABCMeta, abstractmethod

logger = logging.getLogger(__name__)

from Comunication.Client import client
from Filesystem.TransportAgent import agent


class ManagerInterface(metaclass=ABCMeta):
    '''
    The Interface the Comm method must Implemented in order to allow management
    '''
    def sync(self, source, target, dryRun=True):
        '''
        finds all differences between source and target
        '''
        sourceFolder = client().get(source)
        targetFolder = client().get(target)
        transportList = sourceFolder.sync(targetFolder)
        if False == dryRun:
            agent().add(transportList)
        return transportList
