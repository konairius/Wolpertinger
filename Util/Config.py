'''
Created on Jan 24, 2013

'''

import logging
logger = logging.getLogger(__name__)

import configparser
from multiprocessing import Event


def config():
    global _config
    try:
        return _config
    except NameError:
        _config = Config()
        return _config


def registerComMethodes():
    config().registerComMethodes()


class Config(object):

    def __init__(self, configPath='wolpertinger.conf'):
        self.config = configparser.ConfigParser()
        self.config.read(configPath)
        self.loglevel = 'INFO'
        self.logfile = 'wolpertinger.log'

    def registerComMethodes(self):
        from Comunication.Server import server as masterServer
        from Comunication.Client import client as masterClient
        from Comunication.Pyro import Server as PyroServer
        from Comunication.Pyro import Client as PyroClient

        if self.config['Global']['Comm'] == 'Pyro':
            masterServer().register(PyroServer)
            masterClient().register(PyroClient)

    @property
    def stopEvent(self):
        try:
            return self._stopEvent
        except AttributeError:
            self._stopEvent = Event()
            return self._stopEvent

    @property
    def loglevel(self):
        return self._loglevel

    @loglevel.setter
    def loglevel(self, val):
        self._loglevel = val

    @property
    def logfile(self):
        return self._logfile

    @logfile.setter
    def logfile(self, val):
        self._logfile = val

    @property
    def cachePath(self):
        return self.config['Global']['Cachepath']

    @property
    def updateOlder(self):
        return self.config['Global']['OverwriteOlder'] == 'Yes'

    @property
    def servicename(self):
        return self.config['Global']['Servicename']

    @property
    def sharedKey(self):
        try:
            return bytes(self.config['Global']['SharedKey'], 'UTF-8')
        except KeyError:
            return None

    @property
    def publicAddress(self):
        return self.config['Global']['Address']

    @property
    def exposedFolders(self):
        folders = dict()
        for share in self.config.keys():
            if not share in ['Global', 'DEFAULT']:
                folders[share] = self.config[share]['path']
        return folders

    @property
    def transportDir(self):
        return self.config['Global']['TransportDir']

    @property
    def workerThreads(self):
        try:
            return int(self.config['Global']['WorkerThreads'])
        except KeyError:
            return 1
