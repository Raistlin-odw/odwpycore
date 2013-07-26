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
    def __init__(self,exrPath):
        self._exrFile = None
        self._header = None
        self.setExr(exrPath)
        #self._resolution = None
        #self._channel = None
        pass

    def setExr(self,filepath):
        """
        init the exr file 
        @param: filepath,the Exr image path
        @type: string
        """
        try:
            self._exrFile = OpenEXR.InputFile(filepath)
        except IOError,e:
            print("Invalid input file : {0}".format(e))
        self._header = self._exrFile.header()

    @property
    def resolution(self):
        """
        for property self._resolution get
        get resolution from exr file Header

        @return: (x,y)
        @rtype: tuple
        """
        xmax = self._header['dataWindow'].max.x
        xmin = self._header['dataWindow'].min.x
        ymax = self._header['dataWindow'].max.y
        ymin = self._header['dataWindow'].min.y
        self._x = xmax - xmin + 1
        self._y = ymax - ymin + 1
        return (self._x,self._y)

    @resolution.setter
    def setRes(self):
        """
        for property self._resolution set
        empty
        """
        pass

    @resolution.deleter
    def delRex(self):
        """
        for property self._resolution set
        empty
        """
        pass

    @property
    def channel(self):
        """
        get Channel name from exr file header
        @return: a string list with channel name,like ['A','R','G','B']
        @rtype: list
        """
        return self._header['channels'].keys()

    @channel.setter
    def setChannel(self):
        """
        for property self._channel set
        empty
        """
        pass

    @channel.deleter
    def delChannel(self):
        """
        for property self._channel set
        empty
        """
        pass

    def arrayType(self,channel):
        """
        @param:channel,channel name
        @type:string
        @return: the channel data type string for array moudle
                if channel name error return None
        @rtype: string or None
        """
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

        #print("rType is {0}".format(rType))

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

        channelData = self._exrFile.channel(channel)
        #print(channelData[:15])

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
        if channel not in self._header['channels'].keys():
            raise ValueError,'error channel name'
        dataSha1 = self.getExrChannelDataSha1(channel)
        res = self.resolution
        aType = self.arrayType(channel)
        #print aType
        #print res
        fakeSha1 = self.genarateChannelDataSha1(res[0],res[1],aType)
        #print(dataSha1)
        #print(fakeSha1)
        print (dataSha1 == fakeSha1)
        return dataSha1 == fakeSha1

    def isColorBlank(self):
        """
        check whether the channel is blank
        
        @return: true if channel is empty,false if it is not
        @rtype: bool
        """
        keysList = self._header['channels'].keys()
        if ("R" not in keysList) 
            or ("G" not in keysList)
            or ("B" not in keysList):
            raise ValueError,"invalid color Channel :{0}".format(keysList)
        if self.isChannelBlank("R") and self.isChannelBlank("G") and self.isChannelBlank("B"):
            return True
        else:
            return False
        pass