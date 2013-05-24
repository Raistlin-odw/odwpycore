"""
Created on 2013-5-21

@author: hongloull
"""
#/usr/bin/env python2.6
# -*- coding:utf-8 -*-

import odwlib.rv.rvio as rvio
reload(rvio)
    
def main(inMov, frame=1, outputFormat='jpg', outImage=None):
    rvio.getImageFromMov(inMov, frame, outputFormat, outImage)
        
if __name__ == '__main__' :
    import sys
    main(sys.argv[1:])
    


