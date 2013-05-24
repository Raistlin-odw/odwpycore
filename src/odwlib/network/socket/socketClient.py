'''
Created on 2013-5-24

@author: lavenda
'''

#!/usr/bin/env python2.6
# -*- coding:utf-8 -*-


from socket import AF_INET
from socket import SOCK_STREAM
from socket import socket


def connect(data, host, port=21567, bufsiz=1024):
    """
    connect to the socket server and send some datas to it.
    
    @param data: the string you want to send, 
    @type data: string type
    @param host: the destination you want to connect, eg. 192.168.16.4
    @type host: string type
    @param port: the port of the computer you want to connect, eg. 21567
    @type port: int type(default:21567)
    @param bufsiz: the bytes of the message you want to send, eg. 1024
    @type bufsiz: int type(default:1024)
    """
    address = (host, port)
    
    while True:
        tcpCliSock = socket(AF_INET, SOCK_STREAM)   #this module only 
        tcpCliSock.connect(address)
        if not data:
            break
        tcpCliSock.send(data)
        data = tcpCliSock.recv(bufsiz)
        if not data:
            break
        print data.strip()
        tcpCliSock.close()
        

def main():
    pass


if __name__ == '__main__':
    main()