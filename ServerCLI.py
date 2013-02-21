#!/usr/bin/env python3

'''
Created on Jan 26, 2013

@author: konsti
'''

import logging
import argparse
import time

from Comunication.Server import server
from Util.Config import config


def main():

    global shutdown

    shutdown = False

    FORMAT = "%(asctime)s | %(levelname)s | %(name)s: %(message)s"

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
        logging.basicConfig(level=logging.DEBUG)
    elif args.loglevel.upper() == 'INFO':
        logging.basicConfig(level=logging.INFO)
    elif args.loglevel.upper() == 'WARNING':
        logging.basicConfig(level=logging.WARNING)
    elif args.loglevel.upper() == 'ERROR':
        logging.basicConfig(level=logging.ERROR)

    if not args.logfile == 'stdout':
        logging.basicConfig(filename=args.logfile)
        logging.basicConfig(format=FORMAT)

    #WTConfig.Config(args.configfile)

    config().registerComMethodes()

    for key in config().exposedFolders.keys():
        server().add(config().exposedFolders[key], key)
    while False == shutdown:
        if 'quit' == input('#:'):
            shutdown = True
            server().close()
        time.sleep(10)


if __name__ == '__main__':
    main()
