"""
some tools used RVIO
Created on 2013-5-23

@author: hongloull
"""
#/usr/bin/env python2.6
# -*- coding:utf-8 -*-

def getImageFromMov(inMov, frame=1, outputFormat='jpg', outImage=None):
    """
    output image from input movie
    @param inMov: input movie
    @type inMov: str
    @param frame: output frame
    @type frame: int
    @param outputFormat: output image's format
    @type outputFormat: str      
    """
    
    if not outImage:
        import os
        outImage = '%s.%s' % (os.path.splitext(inMov)[0], outputFormat)
    cmd = 'rvio {inputMov} -t {time} -o {ouputImage}'.format(inputMov=inMov, \
                                                             time=frame, \
                                                             outputImage=outImage)
    os.popen(cmd)

