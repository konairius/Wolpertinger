'''
Created on Nov 22, 2012

'''

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.0.1'


import logging
logger = logging.getLogger(__name__)

import xml.dom.minidom as DOM


class MessageParser(object):

    def __init__(self, message):
        self.knownMethodes = ['RemoteMethodCall',
                              'RemoteMethodResponse',
                              'RemoteError']
        self.message = message
        self.parseFlags()
        self.extract()
        self.parseXml()

    def parseFlags(self):
        self.flags = dict()
        flagstrings = self.message[:self.message.find('<')].split(';')
        for flag in flagstrings:
            if -1 != flag.find(':'):
                flag = flag.split(':')
                self.flags[flag[0]] = flag[1]

    def getFlag(self, flag):
        return self.flags[flag]

    def extract(self):
        message = self.message
        try:
            if self.getFlag('secure'):
                raise NotImplementedError
        except(KeyError):
            logger.info('got unencrypted message')

        try:
            if self.getFlag('gzip'):
                raise NotImplementedError
        except(KeyError):
            logger.info('got uncompressed message')

        try:
            if self.getFlag('signature'):
                logger.info('message signing is nyi, will be ignored')
                message = message.split(';')[-1]
        except(KeyError):
            logger.info('got unsigned message')

        self.xml = DOM.parseString(message)

    def parseXml(self):
        if self.xml.nodeName in self.knownMethodes:
            self.type = self.xml.nodeName

            if self.type == 'RemoteMethodCall':
                pass
            elif self.type == 'RemoteMethodResponse':
                pass
            elif self.type == 'RemoteMethodError':
                pass


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
