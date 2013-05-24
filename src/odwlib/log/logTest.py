"""
Created on 2013-5-21

@author: hongloull
"""
#/usr/bin/env python2.6
# -*- coding:utf-8 -*-

import odwlib.log.log as log
reload(log)
    
def sumFunc(*args):
    """
    This method is used to get sum of input arguments.
        
    """
    s = sum(args)
    print s
    return s
        
def logTest():
    """
    test log without decorator
    """
    
    a = log.Log()
    a.createStreamLogger()
    a.Log.debug('debug test')
    
def logTestWithDecorator():
    """
    test log with decorator
    """
    
    @log.log(None,'debug')
    def sumFunc(*args):
        """
        This method is used to get sum of input arguments.
        
        @param : 
        @type : 
        @return: 
        @see: 
            
        """
        s = sum(args)
        print s
        return s
    sumFunc(1,3,5)
 
def logTestCommandline():
    # For pyhon2.6, add argparse from 2.7 version
    try:
        import argparse
    except ImportError:
        import odwpycore.src.odwcore.argparse as argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-debug", "--debug", action="store_true",
                        help="debug mode")
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    args = parser.parse_args()
    if args.debug:
        print args.integers
        #main(args.integers)
        sumFunc(args.integers)
 
# simple test
logTest()
    
# test with decorator
logTestWithDecorator()
    
# command line test
# how to test: python logTest.py -debug 1 3 5           
if __name__ == '__main__' :
    logTestCommandline()
    

