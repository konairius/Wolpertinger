'''
Created on Nov 22, 2012

'''

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.0.1'

import logging
logger = logging.getLogger(__name__)


class MessageParser(object):

    def __init__(self, message):
        self.message = message
        self.parsFlags()

    def parsFlags(self):
        self.flags = dict()
        try:
            flagstrings = self.message[:self.message.index('<')].split(';')
        except(ValueError):
            flagstrings = self.message.split(';')
            logger.warning('got message with out data')
            #return
        for flag in flagstrings:
            flag = flag.split(':')
            self.flags[flag[0]] = flag[1]

    def getFlag(self, flag):
        return self.flags[flag]


class Server(object):
    '''
    classdocs
    '''

    def __init__(self, address, port):
        '''
        Constructor
        '''


class Client(object):
    '''
    classdocs
    '''

    def __init__(self, address, port):
        '''
        Constructor
        '''
