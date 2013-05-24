'''
Created on 2013-5-24

@author: lavenda
'''

#!/usr/bin/env python2.6
# -*- coding:utf-8 -*-


from odwlib.network.socket import socketServer
from odwlib.network.socket import socketClient


def serverTest():
    socketServer.start()
    
    
def connectTest():
    data = 'a'
    host = 'localhost'
    socketClient.connect(data, host)
    
    
if __name__ == '__main__':
    connectTest()
