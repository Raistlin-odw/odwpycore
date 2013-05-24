"""
Created on 2013-5-8

@author: lavenda

@note: 
    This module is the templates of unittest TestCase
    Now, there is only the 'assertEqual' function in this template.
    In future, there are more and more template will be created and offerded
    
"""
#!/usr/bin/env python2.6
# -*- coding:utf-8 -*-

CLASS_TEMPLATE = u"""
import unittest
class MyClass(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    {METHODS_REPLACE}
    
if __name__ == '__main__':
    unittest.main()
"""


METHOD_TEMPLATE = u"""

    def test{NAME_REPLACE}(self):
        self.assertEqual({APPLY_REPLACE}, {RESULT_REPALCE})

"""


methods = u"""""" 
"""
- methods: the big string contains all the string of methods and function you want to test
"""

def buildMethod(func, result, args, kwargs):
    """
    Build the method template and append into the methods.
    
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
    applyStr = u'%s(*args_%s, **kwargs_%s)' % (funcName, funcName, funcName)
    resultStr = result.__str__().decode('utf-8')
    method = METHOD_TEMPLATE.replace('{NAME_REPLACE}', funcName)
    method = method.replace('{APPLY_REPLACE}', applyStr)
    method = method.replace('{RESULT_REPALCE}', resultStr)
    global methods
    methods += method


def buildClass():
    """
    Build the class template with the 'methods' unicode string.
    """
    global methods
    classStr = CLASS_TEMPLATE.replace('{METHODS_REPLACE}', methods)
    return classStr
