"""
Created on 2013-5-13

@author: lavenda
"""

#!/usr/bin/env python2.6
# -*- coding:utf-8 -*-

import os
import ctypes
import shutil
import filecmp
from ctypes.wintypes import MAX_PATH
import fileOper


class EnvPrecheck(object):

    
    SERVER = ['//server-cgi/project']
    MAYA_ENV_FILE = ['//server-cgi/workflowtools_ep20/Install/Maya.env']
    SHAVENODE_FILE = [('C:/Program Files/JoeAlter/shaveHaircut/'
                       'maya2012/plug-ins/shaveNode.mll')]
    SOURCEIMAGE_FOLDER = ['//server-cgi/Project/E020DW/DWep20/sourceimages']
    PLUGIN_FOLDER = ['//server-cgi/workflowtools_ep20']
    
    MAYA_VERSION = '2012-x64'
    RENDERFARM_ACCOUNT_NAME = 'renderfarm'
    
    def __init__(self):
        self.resultStrList = []


    def precheck(self):
        """
        Precheck the maya environment and maya file whether is right.
        There are five steps:
            1. check whether can connect the Server.
            2. check whether the maya env file is right.
            3. check whether the ShaveNode.mll file is right.
            4. check whether the texture files is readable.
            5. check whether the plugin folder is readable.
        And a single step:
         - check whether the maya file is readable.
        
        @return: a string type, contains all the results from every check.
        """
        isAllRight = True
#        if not self._checkServer():
#            self._writeIntoResultStringByType('SdiskConnectError')
#            return 'SdiskConnectError'
#            return False
        self._writeIntoResultStringByType('*********************'
                                          '*********************')
        if not self._checkRenderMayaEnvFile():
            self._writeIntoResultStringByType('MayaEnvError', 
                                              'error')
#            return 'MayaEnvError'
            isAllRight = False
        if not self._checkMayaShaveNodeFile():
            self._writeIntoResultStringByType('ShaveNodeFileError', 
                                              'error')
#            return 'ShaveNodeFileError'
            isAllRight = False
        if not self._checkSourceImagesOnServer():
            self._writeIntoResultStringByType('SourceImagesOnServerError', 
                                              'error')
#            return 'SourceImagesOnServerError'
            isAllRight = False
        if not self._checkPluginFolderOnServer():
            self._writeIntoResultStringByType('PluginFolderError', 
                                              'error')
#            return 'PluginFolderError'
            isAllRight = False
        self._writeIntoResultStringByType('*********************'
                                          '*********************')
        
        return isAllRight
    
    
    def backResultStrList(self):
        """
        back a list of the every check result. 
        """
        return self.resultStrList
    
    
    def _writeIntoResultStringByType(self, resultStr, strType='root'):
        """
        take the result string into a result list by its type
        
        @param resultStr: a result string from a check
        @type resultStr: string type
        @param strType:  a type string of messages to print style.
        @type strType: string type
        
        """
        if strType == 'l1':
            self.resultStrList.append('    ' + resultStr)
        elif strType == 'l2':
            self.resultStrList.append('        ' + resultStr)
        elif strType == 'error':
            self.resultStrList.append('Error: ' + resultStr)
        elif strType == 'warning':
            self.resultStrList.append('Warning: ' + resultStr) 
        else:
            self.resultStrList.append(resultStr)


    def _checkServer(self):
        """
        check whether can connect the Server.
        """
        return self._isExistAndOpenInList(self.SERVER)
    
    
    def _isExistAndOpenInList(self, pathList):
        """
        Overwrite the isExistAndOpen function in fileOper.
        Now it is checking whether the path is readable.
        """
        for path in pathList:
            if fileOper.isExistAndOpen(path):
                self._writeIntoResultStringByType('<%s> ......READ OK' 
                                                  % path, 'l2')
                return path
            else:
                self._writeIntoResultStringByType('<%s> ......READ Failure' 
                                                  % path, 'error')
        return None 
    
    
    def _checkRenderMayaEnvFile(self):
        """
        only check the maya env file in render farm account.
        """
        
        userDocumentsPath = self._getUserDocuments()
        myMayaEnvFile = os.path.join(userDocumentsPath, 'maya',
                                     self.MAYA_VERSION, 'maya.env')
        currentAccount = userDocumentsPath.encode('utf-8').split('\\')[2]
        
        self._writeIntoResultStringByType('*** <%s> is current account. ***' 
                                    % currentAccount)
        self._writeIntoResultStringByType('-> check the Maya Env File', 'l1')
        self._checkAndCopyMayaEnvFile(myMayaEnvFile)
        
        isRight = self._checkMayaEnvFile(myMayaEnvFile)
        if isRight:
            return isRight
        else:
            if self.RENDERFARM_ACCOUNT_NAME in userDocumentsPath:
                if self._copyAndBackupMayaEnvFile(myMayaEnvFile):
                    isRight = self._checkMayaEnvFile(myMayaEnvFile)
            else:
                self._writeIntoResultStringByType(('the current account is '
                                                  'not <RENDERFARM_ACCOUNT>'),
                                                  'warning')
        
        return isRight
    
    
    def _checkAndCopyMayaEnvFile(self, myMayaEnvFile):
        """
        check the maya env file is exist or not.
        if not exist, will copy it from server.
        """
        if not os.path.isfile(myMayaEnvFile):
            self._writeIntoResultStringByType('<%s> is not exist'
                                        % myMayaEnvFile, 'error')
            self._copyMayaEnvFile(myMayaEnvFile)
    
    
    def _checkMayaEnvFile(self, myMayaEnvFile):
        """
        check whether the maya env file is right.
        """
        if not fileOper.isExistAndOpen(myMayaEnvFile):
            return False
        mayaEnvFile = self._isExistAndOpenInList(self.MAYA_ENV_FILE)
        if not mayaEnvFile:
            return False
        
        try:
            isSame = filecmp.cmp(mayaEnvFile, myMayaEnvFile)
            if not isSame:
                self._writeIntoResultStringByType('<%s> is not right' 
                                                  % myMayaEnvFile, 'error')
                return False
        except:
            self._writeIntoResultStringByType('open maya env error', 'error')
        self._writeIntoResultStringByType('<%s> ...... CHECK OK' 
                                                % myMayaEnvFile, 'l2')
        return True
    
    
    def _copyAndBackupMayaEnvFile(self, myMayaEnvFile):
        """
        backup the local maya env file,
        and copy the maya env file from server to local
        """
        try:
            reName = myMayaEnvFile + '.bak'
            shutil.move(myMayaEnvFile, reName) 
        except:
            self._writeIntoResultStringByType('backup maya env file error',
                                              'error')
            return False
        
        return self._copyMayaEnvFile(myMayaEnvFile)

    
    def _copyMayaEnvFile(self, myMayaEnvFile):
        """
        copy the maya env file from server to local
        """
        try:
            shutil.copy(self.MAYA_ENV_FILE[0], myMayaEnvFile)
        except:
            self._writeIntoResultStringByType('copy maya env file error',
                                              'error')
            return False
        self._writeIntoResultStringByType('<%s> copy completed' % myMayaEnvFile,
                                          'warning')
        return True
    
    
    def _getUserDocuments(self):
        """
        get user's documents:
        Example: C:\Users\username\Documents
        """
        dll = ctypes.windll.shell32
        buf = ctypes.create_unicode_buffer(MAX_PATH + 1)
        if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
            #print(buf.value)
            return buf.value
        else:
            self._writeIntoResultStringByType('get user documents Failure!',
                                              'error')
            return None
    
    
    def _checkMayaShaveNodeFile(self):
        """
        check whether the ShaveNode.mll file is right.
        """
        self._writeIntoResultStringByType('-> check Maya ShaveNode File', 'l1')
        return self._isExistAndOpenInList(self.SHAVENODE_FILE)
    
    
    def _checkSourceImagesOnServer(self):
        """
        check whether the texture files is readable.
        """
        self._writeIntoResultStringByType('-> check Source Images On Server',
                                          'l1')
        sourceimagesFolder = self._isExistAndOpenInList(self.SOURCEIMAGE_FOLDER)
        if not sourceimagesFolder:
            return False
        for element in os.listdir(sourceimagesFolder):
            elementPath = os.path.join(sourceimagesFolder, element)
            if not fileOper.isExistAndOpen(elementPath): 
                return False
            
        return True
    

    def _checkPluginFolderOnServer(self):
        """
        check whether the plugin folder is readable.
        """
        self._writeIntoResultStringByType('-> check Plugin Folder On Server',
                                          'l1')
        return self._isExistAndOpenInList(self.PLUGIN_FOLDER)

    
    def checkMayaFile(self, mayaFile):
        """ 
        check whether the maya file is readable.
        """
        if not self._checkMayaFile(mayaFile):
            self._writeIntoResultStringByType('<%s>MayaFileError' 
                                        % mayaFile, 'error')
            return False
        
        return True

    
    def _checkMayaFile(self, mayaFile):
        """
        check whether the maya file is readable.
        """
        return fileOper.isExistAndOpen(mayaFile)
    


def main():
    epCls = EnvPrecheck()
    print epCls.precheck() 
    print '\n'.join(epCls.backResultStrList())

if __name__ == '__main__':
    main()
