#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
"""
Created on 2013-6-25

@author: Raistlin.Chen
@version: 0.1
"""

import sys
import array
import OpenEXR
import Imath
import os
from hashlib import sha1


class ExrCheck(object):
    """
    OpenExr black channel check 
    """
    def __init__(self):
        self._exrFile = None
        self._header = None
        pass

    def setExr(self,filepath):
        """
        1.check filepath exists
        2.do exr check first to make sure the input filepath IS a exr image
        3.set it as target
        @param: filepath,the Exr image path
        @type: string

        @rtype: bool
        @return: Return True if filepath is a exr image. 
        Returns False if filepath is not a exr image or not exists  
        """
        if not os.path.exists(filepath):
            print '%s not exists'%filepath
            return False


        if not OpenEXR.isOpenExrFile(filepath):
            print 'the %s is not a exr file'%filepath
            return False

        else:
            self._exrFile = OpenEXR.InputFile(filepath)
            self._header = self._exrFile.header()
            return True

    def isExrSet(self):
        """
        check whether the exr image has been set to self._exrFile
        @return: Return True if self._exrFile and self._header have been set
        return False if self._exrFile and self._header are empty
        """
        if (not self._exrFile) or (not self._header):
            return False
        else:
            return True

    def getRes(self):
        """
        get resolution from exr file Header

        @return: (x,y)
        @rtype: tuple
        """
        if not self.isExrSet():
            return None
        
        xmax = self._header['dataWindow'].max.x
        xmin = self._header['dataWindow'].min.x
        ymax = self._header['dataWindow'].max.y
        ymin = self._header['dataWindow'].min.y
        self._x = xmax - xmin + 1
        self._y = ymax - ymin + 1
        return (self._x,self._y)

    def getChannel(self):
        """
        get Channel name from exr file header
        @return: a string list with channel name,like ['A','R','G','B']
        @rtype: list
        """
        
        return self._header['channels'].keys()

    def arrayType(self,channel):
        """
        @param:channel,channel name
        @type:string
        @return: the channel data type string for array moudle
                if channel name error return None
        @rtype: string or None
        """
        if not self.isExrSet():
            return None
        if channel not in self._header['channels'].keys():
            print 'error channel name'
            return None

        channelTypeV = self._header['channels'][channel].type.v
        rType = None

        if channelTypeV == Imath.PixelType(OpenEXR.HALF).v:
            #c type float
            rType = 'h'
        if channelTypeV == Imath.PixelType(OpenEXR.FLOAT).v:
            #c type double float
            rType = 'f'
        if channelTypeV == Imath.PixelType(OpenEXR.UINT).v:
            #c type unsigned long
            rType = 'L'
        print 'rType is ',rType

        return rType



    def genarateChannelDataSha1(self,x,y,dType):
        """
        simulation a fake ,blank channel data and get the sha1 code for Comparing
        @param: x
        @type:string
        @return: the fake data's sha1 code
        @rtype: string
        """
        if dType in ['f']:
            dataString = array.array('f', [ 0.0 ] * (x * y )).tostring()

        #cheat here,python do not have half float 16bit
        if dType in ['h']:
            dataString = array.array('f', [ 0.0 ] * (x * y /2)).tostring()            

        if dType in ['L']:
            dataString = array.array(dType, [0] * (x * y)).tostring()
        print dataString[:15]
        h = sha1()
        h.update(dataString)
        return h.hexdigest()

    def getExrChannelDataSha1(self,channel):
        """
        get the sha1 code from the exr image
        @param: channel
        @type: string
        @return: sha1 code from exr image channel
        @rtype: string
        """
        if not self.isExrSet():
            return None
        if channel not in self._header['channels'].keys():
            print 'error channel name'
            return None  
        channelData = self._exrFile.channel(channel)
        print channelData[:15]

        #print type(arrayStr)
        h = sha1()
        h.update(channelData)
        return h.hexdigest()

    def isChannelBlank(self,channel):
        """
        check whether the channel is blank
        @param: channel
        @type: string
        @return: true if channel is empty,false if it is not
        @rtype: bool
        """
        dataSha1 = self.getExrChannelDataSha1(channel)
        res = self.getRes()
        aType = self.arrayType(channel)
        #print aType
        fakeSha1 = self.genarateChannelDataSha1(res[0],res[1],aType)
        print dataSha1
        print fakeSha1
        if dataSha1 == fakeSha1:
            return True
        else:
            return False






















