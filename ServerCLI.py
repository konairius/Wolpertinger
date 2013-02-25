#!/usr/bin/env python3

'''
Created on Jan 26, 2013

@author: konsti
'''

import argparse

from Comunication.Server import server
from Util.Config import config


def main():

    parser = argparse.ArgumentParser(prog='Wolpertinger',
                                     description='Start a wolpertinger server.')
    parser.add_argument('--loglevel', dest='loglevel', default='INFO',
                        help='DEBUG, INFO, WARNING or ERROR')
    parser.add_argument('--logfile', dest='logfile', default='wolpertinger.log',
                        help='typically /var/log/wolpertinger.log')
    parser.add_argument('--configfile', dest='configfile', default='wolpertinger.conf',
                        help='check wolpertinger.conf.example for reference')

    args = parser.parse_args()

    if args.loglevel.upper() == 'DEBUG':
        config().loglevel = 'DEBUG'
    elif args.loglevel.upper() == 'INFO':
        config().loglevel = 'INFO'
    elif args.loglevel.upper() == 'WARNING':
        config().loglevel = 'WARNING'
    elif args.loglevel.upper() == 'ERROR':
        config().loglevel = 'ERROR'

    config().logfile = args.logfile

    import Util.Logger

    config().registerComMethodes()

    for key in config().exposedFolders.keys():
        server().add(config().exposedFolders[key], key)
    while False == config().stopEvent.is_set():
        if 'quit' == input('#:'):
            config().stopEvent.set()
            server().close()
        #time.sleep(10)


if __name__ == '__main__':
    main()
