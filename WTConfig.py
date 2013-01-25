'''
Created on Jan 24, 2013

'''

import logging
logger = logging.getLogger(__name__)

import configparser


def getConfig():
    try:
        return config
    except NameError:
        Config()
        return config


class Config(object):
    
    def __init__(self, configPath='wolpertinger.conf'):
        global config
        self.config = configparser.ConfigParser()
        self.config.read(configPath)
        config = self
    
    def getFileCache(self):
        return self.config['Filecache']['Path']
    
    
    def updateOlder(self):
        return self.config['Sync']['Overwrite Older'] == 'Yes'
    
    
    def getServicename(self):
        return self.config['Sync']['Servicename']
    
    def getSharedKey(self):
        try:
            return bytes(self.config['Sync']['SharedKey'],'UTF-8')
        except KeyError:
            return None
        
    def getPublicAddress(self):
        return self.config['Sync']['Address']
