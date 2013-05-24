"""
Created on 2013-5-3

@author: huangchengqi
"""
from time import sleep
class Test(object):
    """
    classdocs
    """

    num = 0
    def __init__(self):
        """
        Constructor
        """
        pass
    def range3(self):
        for i in range(3):
            sleep(1)
            print i
        print 'range10 has done'
    
    def range10(self):
        for i in range(10):
            print i
        print 'range10 has done'
    
    
    def range100(self):
        for i in range(100):
            print i
        print 'range100 has done'
        
    
    def range10000(self, str):
        for i in range(10):
            print str
#            print i
#            self.num += 1
#            pass
#        print 'range10000 has done'
        
def range10000(str):
    for i in range(10):
        print str

from time import clock as now 
if __name__ == '__main__':
    start = now()
    test = Test()
#    print str(type(test.range10))=="<type 'instancemethod'>"
#    print isinstance(test.range10,)
    for i in range(300):
        test.range10000(str='a')
    finish = now() 
    print (finish - start) 
    
