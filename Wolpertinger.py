#!/usr/bin/env python
# -*- coding: ascii -*-

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.0.1'

import logging
import argparse
from WTlib import WTConnection
from WTlib import WTTransport
from WTlib import WTTransport_cp
from WTCom import Local

logger = logging.getLogger(__name__)


FORMAT = "%(asctime)s | %(levelname)s | %(name)s: %(message)s"

logging.basicConfig(format=FORMAT,
                    level=logging.DEBUG)


def main():
    parser = argparse.ArgumentParser(description='Wolpertinger CLI')
    parser.add_argument('source', metavar='Source', help='the source path')
    parser.add_argument('target', metavar='Target', help='the target path')

    args = vars(parser.parse_args())
    URI = 'localhost'
    connection = WTConnection.Connection(URI, URI)
    connection.sync(args['source'], args['target'])
    logger.info('Finshed calculating changes starting copy')
    WTTransport.block()


if __name__ == '__main__':
    WTTransport.register(WTTransport_cp.cpProvider)
    WTConnection.register(Local.localCom)
    main()
