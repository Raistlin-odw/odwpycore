"""
Created on 2013-5-8
 
@author: lavenda

This module uses the unittest module and decorator to achieve fast unit test.
You can write and test the code in the meantime.
The result in Console is the results that you write a PyUnit TestCase by yourself.

@note: 
Like follows:
  eg.:
    from decorator import myPyUnit   {-------> You must import module}

    class unit(object):
        
        def __init__(self):
            self.a = 'a' 
            
        @myPyUnit.myTest(result=3,a='a',b=3)  {-----> You can add '@' above a method}
        def func(self,a, b):
            return a+b
        
        @myPyUnit.myTest(result=1,b=3,c=3)
        def func2(self,b,c):
            d = b/c
            self.func3(a='a',b=3)
            return d
        
        def func3(self,a,b):
            return a/b

    @myPyUnit.myTest(3,1,2)  {-----> You can add '@' above a function}
    def func(a, b):
            return a+b

    if __name__=='__main__':
        myPyUnit.run(globals())    {------>You must use 'myPyUnit.run()' to start the unittest}
        
- There are two point:
    1. If your test method is a class's method,
     you must give the attribute name like this({@myPyUnit.myTest(result=3,b=1,c=2)}).
     If it is only a function, you can also use all the way, such as ({@myPyUnit.myTest(3,1,2)})
    2. It cannot be used to a class, and it is only for methods or functions.
    
"""

#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
from odwlib.unitTest import myUnitTemplate
import types

""" 
- unitGlobals: the globals information of the test module.
"""
unitGlobals = {}


def __addGlobals(func, result, args, kwargs):
    """
    Add the data of func to the globals().
    
    @param func: the function or method object.
    @type func: the function or method object type
    @param result: the result of the function or the method you want to test.
    @type result: any type
    @param args: the arguments of func
    @type args: list type
    @param kwargs: the arguments of func
    @type kwargs: dictionary type
    
    """
    funcName = func.__name__.decode('utf-8')
    global unitGlobals
    unitGlobals[funcName] = func
    unitGlobals['result_'+funcName] = result
    unitGlobals['args_'+funcName] = args
    unitGlobals['kwargs_'+funcName] = kwargs


def __buildUnit(func, result, args, kwargs):
    """
    Build a unit by a unit template from string in myUnitTemplate.
    
    @param func: the function or method object.
    @type func: the function or method object type
    @param result: the result of the function or the method you want to test.
    @type result: any type
    @param args: the arguments of func
    @type args: list type
    @param kwargs: the arguments of func
    @type kwargs: dictionary type
    
    """
    if isinstance(result, types.StringType):
        result = "'%s'" % result
    myUnitTemplate.buildMethod(func, result, args, kwargs)
    __addGlobals(func, result, args, kwargs)
    
    
    
def __testUnit():
    """
    Run all the unit tests, when all has been built.
    
    """
    global unitGlobals
    classStr = myUnitTemplate.buildClass()
    exec classStr in unitGlobals


def __classRun(className, classType):
    """
    Get all the method which want to be test in '__main__' class,
    and build it into the template.
    
    @param className: the name of class
    @type className: string type
    @param classType: a class element.
    @type classType: class type
    
    """
    funcGroup = classType.__dict__.items()
    instance = classType()
    if not '__main__' in str(classType):
        return
    for funcName, funcObject in funcGroup:
        if funcName.startswith('__') and funcName.endswith('__'):
            continue
        if not isinstance(funcObject, types.FunctionType):
            continue
        innerFuncName = funcObject.__name__
        if innerFuncName == '__myTest' or innerFuncName == '_myTest':
            funcObject(instance)


def __functionRun(funcName, funcObject):
    """
    Get all the function which want to be test in '__main__' module,
    and build it into the template.
    
    @param className: the name of function
    @type className: string type
    @param classType: a function element.
    @type classType: function type
    
    """
    if funcName.startswith('__') and funcName.endswith('__'):
        return 
    innerFuncName = funcObject.__name__
    if innerFuncName == '__myTest' or innerFuncName == '_myTest':
        funcObject()


def run(testGlobals):
    """
    This function is the switch of the unittest.
    
    @param testGlobals: the globals() environment of the module you want to test.
    @type testGlobals: the globals() dictionary.
    
    """
    global unitGlobals
    unitGlobals = testGlobals
    for name, element in  unitGlobals.items():
        if isinstance(element, types.TypeType):
            __classRun(name, element)
        if isinstance(element, types.FunctionType):
            __functionRun(name, element)
    
    __testUnit()
    
    
def myTest(result=None, *args, **kwargs):
    """
    The decorator implementation class.
    
    @param result: the result of the function or the method you want to test.
    @type result: any type
    
    """
    def _myTest(func):
        
        def __myTest(self=None):
            if self:
                kwargs['self'] = self
            __buildUnit(func, result, args, kwargs)
        return __myTest
    
    return _myTest


if __name__ == '__main__':
    pass