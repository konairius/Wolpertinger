'''
Created on Feb 24, 2013

@author: konsti
'''
import logging
import logging.handlers
import logging.config

from threading import Thread
from queue import  Queue

import Util.Config

loggerQueue = Queue()


class Handler(object):
    '''
    This is the main logging handler for the Wolpertinger Project
    '''
    def handle(self, record):
        logger = logging.getLogger(record.name)
        logger.handle(record)


def listener():
    '''
    Process handler that starts the listener
    '''
    global loggerQueue

    config = {
              'version': 1,
              'disable_existing_loggers': True,
              'formatters': {
                             'detailed': {
                                          'class': 'logging.Formatter',
                                          'format': '%(asctime)s | %(levelname)s | %(processName)s | %(threadName)s | %(name)s: %(message)s'
                                          },
                             'simple': {
                                        'class': 'logging.Formatter',
                                        'format': '%(asctime)s | %(levelname)s | %(name)s: %(message)s'
                                        }
                             },
              'handlers': {
                           'console': {
                                       'class': 'logging.StreamHandler',
                                       'level': 'INFO',
                                       'formatter': 'simple'},
                           'file': {
                                    'class': 'logging.FileHandler',
                                    'level': 'DEBUG',
                                    'filename': 'wolpertinger.log',
                                    'mode': 'w',
                                    'formatter': 'detailed'}
                           },
              'root': {
                       'level': 'DEBUG',
                       'handlers': ['console', 'file']}
              }
    logging.config.dictConfig(config)
    listener = logging.handlers.QueueListener(loggerQueue, Handler())
    listener.start()
    Util.Config.stopEvent.wait()
    logger.info('Closing Logger')
    listener.stop()


def getLogger(name):
    global loggerQueue
    config = {
              'version': 1,
              'disable_existing_loggers': True,
              'handlers': {
                           'queue': {
                                    'class': 'logging.handlers.QueueHandler',
                                    'queue': loggerQueue},
                           },
              'root': {
                       'level': 'DEBUG',
                       'handlers': ['queue']},
              }

    logging.config.dictConfig(config)
    return logging.getLogger(name)

try:
    loggerThread.is_alive()
except NameError:
    logger = getLogger(__name__)
    logger.info('Staring logger')
    loggerThread = Thread(target=listener, name='loggingListener')
    loggerThread.daemon = True
    loggerThread.start()
