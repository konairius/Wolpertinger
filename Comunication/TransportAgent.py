'''
Created on Feb 4, 2013

@author: konsti
'''

import logging
logger = logging.getLogger(__name__)

from Filesystem.CopyTransport import copyAgent
from Comunication.Client import client


class MasterAgent(object):
    '''
    Main Instance responsible for giving the individual files to the corresponding subAgent
    '''
    def __init__(self):
        pass

    def add(self, transferList):
        '''
        transferList is a list of tuple: (SourceUri, TargetUri)
        '''
        for transfer in transferList:
            sourceItem = client().get(transfer[0])
            targetItem = client().get(transfer[1])
            if sourceItem.uri.isLocal() and targetItem.uri.isLocal():
                copyAgent().add(sourceItem.path, targetItem.path)
                