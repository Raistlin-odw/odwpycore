#/usr/bin/env python2.6
# -*- coding:utf-8 -*-

"""
Created on 2013-5-21

@author: Raistlin
@version: 0.0.1 

"""

import sys
import logging
import inspect
#from scripts.system.log import Log

#sys.path.append(r'D:/py_work/digital37_ep20')

class LogLevel(object):
    """
    LogLevel
        a wrapper for logging

    """
    def __init__(self,*arg,**kwargs):
        self.log = logging.getLogger('')
        #self.log.propagate = False
        #handler = logging.StreamHandler()
        self.handler = logging.handlers.SysLogHandler()
        self.handler.setLevel(logging.INFO)
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)
        
        

    def formated(self):
        self.handler.setFormatter(self.formatter)
        self.log.addHandler(self.handler)
        
    def __doc__(self):
        """from scripts.system.log,direct export log by args

        """
        pass

    def write(self,msg):
        self.log.info(msg)

    def info(self,msg):
        self.log.info(msg)

    def warning(self,msg):
        self.log.warning(msg)

    def critical(self,msg):
        self.log.critical(msg)

    def debug(self,msg):
        self.log.debug(msg)

    def doNothing(self):
        print arg
        print kwargs
        return