'''
Created on 2013-5-24

@author: lavenda
'''

#!/usr/bin/env python2.6
# -*- coding:utf-8 -*-

from SocketServer import ThreadingTCPServer
from SocketServer import StreamRequestHandler
from time import ctime
from odwlib.network.socket import requestHandler


class MyRequestHandler(StreamRequestHandler):
    """
    inherit the StreamRequestHandler, and overwrite it.
    handle the request by hint with my way.
    """
    
    def __init__(self, request, client_address, server):
        StreamRequestHandler.__init__(self, request, client_address, server)
    
    
    def handle(self):
        """
        the handle requests
        """
        print '...connected from:', self.client_address
        hint = self.rfile.readline()
        handleRequestObject = requestHandler.RequestHandler(hint)
        response = handleRequestObject.handle()
        
        if response:
            responseStr = 'has done'
        else:
            responseStr = 'something error'
            
        self.wfile.write('[%s] %s' % (ctime(), responseStr))
        


def start(port=21567):
    """
    this function to start the server, and maintain listening the port.
    """
    host = ''
    address = (host, port)
    tcpServ = ThreadingTCPServer(address, MyRequestHandler)
    print 'waiting for connection...'
    tcpServ.serve_forever()


def stop(port=21567):
    """
    this function to close the server
    """
    host = ''
    address = (host, port)
    tcpServ = ThreadingTCPServer(address, MyRequestHandler)
    print 'closing connection...'
    tcpServ.shutdown()


if __name__ == '__main__':
    pass