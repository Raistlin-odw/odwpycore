"""
Created on 2013-5-21

@author: hongloull
"""
#/usr/bin/env python2.6
# -*- coding:utf-8 -*-

import logging
import time

# IMPORTANT add basic configure for multi-class
#logging.basicConfig(level=logging.DEBUG)

class Log(object):
    """
    """
    LOG_LEVELS = {'debug': logging.DEBUG, 'info':logging.INFO, \
                  'warning': logging.WARNING, 'error': logging.ERROR,\
                  'critical': logging.CRITICAL}
    def __init__(self):
        pass
    
    def createStreamLogger(self,logLevel='debug'):
        """
        create default stream logger
        """

        # create logger
        self.Log = logging.getLogger(time.asctime())
        self.Log.setLevel(Log.LOG_LEVELS.get(logLevel))

        # create console handler and set level to debug
        handler = logging.StreamHandler()
        handler.setLevel(Log.LOG_LEVELS.get(logLevel))
        
        # create formatter
        formatter = logging.Formatter("%(levelname)s %(asctime)s %(message)s")
        
        # add formatter to ch
        handler.setFormatter(formatter)
        
        # add ch to logger
        self.Handler = handler
        self.Log.addHandler(handler)
        
        return self.Log

    def createFileLogger(self,logFile=None,logLevel='debug'):
        """
        create file logger
        """

        self.Log = logging.getLogger(time.asctime())
        self.Log.propagate = False
        
        # use temp file as logger file if user not set
        if not logFile:
            import os
            import tempfile
            fd,logFile = tempfile.mkstemp('.log')
            os.close(fd)

        print 'file_log:%s' % logFile
        self.Log_File = logFile
        handler = logging.handlers.RotatingFileHandler(logFile, maxBytes=2097152, backupCount=5)
        handler.setLevel(Log.LOG_LEVELS.get(logLevel))
        #formatter = logging.Formatter("%(levelname)s %(asctime)s %(message)s")
        formatter = logging.Formatter("%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s")
        handler.setFormatter(formatter)
        self.Log.addHandler(handler)
        self.Handler = handler
           
def log(logger=None,level='debug'):
    """
    This method is used to decorator log input function.
    
    @param logger: logger
    @type func: logger
    @param level: log level
    @type level: str
    @return: 
    """
    def wrap(func):
        """
        This method is used to decorator log input function.
        
        @param func: func name
        @type func: 
        @return: 
        """
        log = logger
        if not log:
            # create default stream log
            log = Log().createStreamLogger(level)
        def func_wrapper(*args, **kwargs):
            log.debug("%s:" % func.__name__)
            for i, arg in enumerate(args):
                log.debug("\targs-%d: %s" % (i + 1, arg))
            for k, v in enumerate(kwargs):
                log.debug("\tdict args: %s: %s" % (k, v))
            return func(*args, **kwargs)
        return func_wrapper
    return wrap
