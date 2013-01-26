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
        return self.config['Global']['Cachepath']

    def updateOlder(self):
        return self.config['Global']['OverwriteOlder'] == 'Yes'

    def getServicename(self):
        return self.config['Global']['Servicename']

    def getSharedKey(self):
        try:
            return bytes(self.config['Global']['SharedKey'], 'UTF-8')
        except KeyError:
            return None

    def getPublicAddress(self):
        return self.config['Global']['Address']

    def getExposedFolders(self):
        folders = dict()
        for share in self.config.keys():
            if not share in ['Global', 'DEFAULT']:
                folders[share] = self.config[share]['path']
        return folders
