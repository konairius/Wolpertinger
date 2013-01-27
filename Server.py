'''
Created on Jan 26, 2013

@author: konsti
'''

import logging
logging.basicConfig(level=logging.DEBUG)
import WTPyro


if __name__ == '__main__':
    m = WTPyro.Manager()
    m.startServer()
    m.exposeFolders()
    while True:
        if 'yes' == input('Shutdown'):
            m.stopServer()
            break
