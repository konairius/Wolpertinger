'''
Created on Jan 24, 2013

'''

import logging
logger = logging.getLogger(__name__)


from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client

import WTFilesystem


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class Server(object):
    '''
    XmlRpc Server waiting for remote Calls
    '''

    def __init__(self, address='localhost', port=8000):
        '''
        Constructor
        '''
        self.server = SimpleXMLRPCServer((address, port),
                            requestHandler=RequestHandler)
        self.server.register_introspection_functions()
        self.server.register_function(WTFilesystem.Folder.fromPath, 'getFolder')

        logger.info('Starting server on:' + address + ':' + str(port))
        self.server.serve_forever()


class Client(object):
    '''
    Handels the Connection with the Server
    '''
    def __init__(self, host='localhost', port=8000):
        self.server = xmlrpc.client.ServerProxy('http://' + host + ':' + str(port))
        if ('getFolder' in self.server.system.listMethods()):
            logger.info('Successfully connected')

    def getFolder(self, path):
        logger.info('Requesting remote path via XMLRPC: ' + path)
        self.server.getFolder(path)
