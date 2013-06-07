'''
Created on 2013-5-13

@author: lavenda
'''
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os


def __dirOper(srcPath, countOfOpen):
    '''
    the directory operation.
    '''
    isFit = True
    for element in os.listdir(srcPath):
        elementPath = os.path.join(srcPath,element)
        if os.path.isfile(elementPath):
#            print element
            isFit = __fileOper(elementPath)
            countOfOpen -= 1
            if countOfOpen == 0:
                break
    return isFit


def __fileOper(srcPath):
    '''
    the file operation.
    '''
    try:
        fileStream = open(srcPath, 'r')
        context = fileStream.read(500)
    except:
        print '%s is error'%srcPath
        return False
    finally:
        fileStream.close()
    if context:
        return True
    else:
        return False


def isExistAndOpen(srcPath, countOfOpenInDir=6):
    '''
    Check the source path is exist or not, and whether is readable.
    
    @param srcPath: the source path
    @type srcPath: string type
    @param countOfOpenInDir: how many file you want to check readable in this folder.
    @type countOfOpenInDir: int type(default:5)
    
    @return: boolean type, means it's exist and readable or not.
    '''
    if os.path.isdir(srcPath):
        return __dirOper(srcPath, countOfOpenInDir)
    elif os.path.isfile(srcPath):
        return __fileOper(srcPath)
    else:
        return None
    




if __name__ == '__main__':
    print isExistAndOpen(srcPath=r'C:\Users\huangchengqi\Desktop\a')