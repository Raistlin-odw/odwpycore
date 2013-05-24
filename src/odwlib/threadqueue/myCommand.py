"""
Created on 2013-5-1

@author: lavenda 
"""
#!/usr/bin/env python2.6
# -*- coding:utf-8 -*- 

class MyCommand(object):
    """
    This class is uesd to package all kinds of method objects, likes a data transfer object.
    
    """

    def __init__(self):
        self.methodObject = None
        self.lock = object
        self.priority = 0
        self.args = []
        self.kwargs = {}
        self.result = None
        
    
    def setCommand(self, methodObject, lock, priority, args, kwargs):
        """
        this method is used to give values to this object's attributes.
        
        @param methodObject: it is a object of the method you want to run.
        @type methodObject: method object
        @param args: it is the args of the method you want to run.
        @type args: list type
        @param kwargs: it is the key-value args of the method you want to run.
        @type kwargs: dictionary type
         
        """
        self.methodObject = methodObject
        self.lock = lock
        self.priority = priority
        self.args = args
        self.kwargs = kwargs
    
     
    def setResult(self, result):
        """
        This mehtod is used to set the result to this object's result after this methodObject ran
        
        @param result: Any type, the result of the method object
        """
        self.result = result
    
    
    def getResult(self):
        """
        This method is used to get the result from this object's attribute.
        - It has many problems in this method, so it will make better in future.
        
        @return: Any type or an exception(None temporarily). If the method has run accurately, 
            it will return a normal result, otherwise it will raise an exception.
        """
        if self.result == None:
            return None     #return None temporarily, 
                            #it should be retruning an exception
        else:
            return self.result
