"""
some tools for system

Created on 2013-5-21

@author: hongloull
"""
#/usr/bin/env python2.6
# -*- coding:utf-8 -*-

def getUserName():
    '''
    return login user name
    '''
    import getpass
    return getpass.getuser()
