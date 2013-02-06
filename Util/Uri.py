'''
Created on Jan 27, 2013

@author: konsti
'''
import logging
logger = logging.getLogger(__name__)

from os import path
from Util.Config import config


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
        if not string.startswith('WT://'):
            raise InvalidURIError(string)
        self.string = string

    def __repr__(self):
        return self.string

    @property
    def exportIdentifier(self):
        return self.string.split('/')[2]

    @property
    def path(self):
        try:
            result = self.string.split('/', 3)[3]
            if '' == result:
                result = '/'
            return result
        except IndexError:
            return '/'

    def append(self, newPart):
        return Uri('WT://' + self.exportIdentifier + path.join(self.path, newPart))

    def contains(self, subUri):
        return subUri.string.startswith(self.string)

    def getNextItem(self, uri):
        result = self.path.lstrip(uri.path).split('/')[0]
        return result

    def __eq__(self, *args, **kwargs):
        try:
            return self.string == args[0].string
        except AttributeError:
            return False

    @property
    def isLocal(self):
        return self.exportIdentifier.split('.')[-1] == config().servicename


class InvalidURIError(Exception):
    pass
