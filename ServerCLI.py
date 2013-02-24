#!/usr/bin/env python3

'''
Created on Jan 26, 2013

@author: konsti
'''

import argparse
import time

from Comunication.Server import server
from Util.Config import config
import Util.Config
import Util.Logger


def main():

    parser = argparse.ArgumentParser(prog='Wolpertinger',
                                     description='Start a wolpertinger server.')
    parser.add_argument('--loglevel', dest='loglevel', default='INFO',
                        help='DEBUG, INFO, WARNING or ERROR')
    parser.add_argument('--logfile', dest='logfile', default='stdout',
                        help='typically /var/log/wolpertinger.log')
    parser.add_argument('--configfile', dest='configfile', default='wolpertinger.conf',
                        help='check wolpertinger.conf.example for reference')

    args = parser.parse_args()

    if args.loglevel.upper() == 'DEBUG':
        Util.Config.loglevel = 'DEBUG'
    elif args.loglevel.upper() == 'INFO':
        Util.Config.loglevel = 'INFO'
    elif args.loglevel.upper() == 'WARNING':
        Util.Config.loglevel = 'WARNING'
    elif args.loglevel.upper() == 'ERROR':
        Util.Config.loglevel = 'ERROR'

    if not args.logfile == 'stdout':
        Util.Config.logfile = args.logfile

    Util.Config.registerComMethodes()

    for key in config().exposedFolders.keys():
        server().add(config().exposedFolders[key], key)
    while False == Util.Config.stopEvent.is_set():
        if 'quit' == input('#:'):
            Util.Config.stopEvent.set()
            server().close()
        #time.sleep(10)


if __name__ == '__main__':
    main()
