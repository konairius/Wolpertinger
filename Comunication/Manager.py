'''
Created on Feb 6, 2013

@author: konsti
'''

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
