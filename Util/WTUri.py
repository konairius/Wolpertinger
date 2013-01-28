'''
Created on Jan 27, 2013

@author: konsti
'''
import logging
logger = logging.getLogger(__name__)

from os import path

import WTConfig


class Uri(object):
    '''
    classdocs
    '''
    @classmethod
    def fromExportIdentifier(cls, export):
        return cls('WT://' + export + '/')

    def __init__(self, string):
        '''
        Format:
        WT://EXPORT.SERVICE/path/to/resource
        '''
        self.config = WTConfig.getConfig()
        if not string.startswith('WT://'):
            raise InvalidURIError(string)
        self.string = string
        self.exportIdentifier = self.string.split('/')[2]
        try:
            self.path = self.string.split('/', 3)[3]
        except IndexError:
            self.path = ''

    def __repr__(self):
        return self.string

    def getExportIdentifier(self):
        return self.exportIdentifier

    def getPath(self):
        if self.path == '':
            return'/'
        return self.path

    def append(self, newPart):
        return Uri('WT://' + self.exportIdentifier + '/' + path.join(self.path, newPart))

    def contains(self, subUri):
        return subUri.string.startswith(self.string)

    def getNextItem(self, uri):
        result = self.getPath().lstrip(uri.getPath()).split('/')[0]
        return result

    def __eq__(self, *args, **kwargs):
        try:
            return self.string == args[0].string
        except AttributeError:
            return False

    def isLocal(self):
        return self.getExportIdentifier().split('.')[-1] == self.config.getServicename()


class InvalidURIError(Exception):
    pass
