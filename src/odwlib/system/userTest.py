"""
some tools for system

Created on 2013-5-21

@author: hongloull
"""
#/usr/bin/env python2.6
# -*- coding:utf-8 -*-


import odwlib.system.user as user
reload(user)

if __name__ == '__main__':
    print user.getUserName()