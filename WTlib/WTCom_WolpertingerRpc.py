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

    def parsFlag(self, flag):
        position = self.message.find(flag)
        value = self.message[position + len(flag) + 1: self.message.find(';', position)]
        return value


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
