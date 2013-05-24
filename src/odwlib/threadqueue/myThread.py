"""
Created on 2013-5-1

@author: lavenda
"""

#!/usr/bin/env python2.6
# -*- coding:utf-8 -*-
from threading import Thread


class MyThread(Thread):
    """
    Inherit from threading.Thread class, and make it more suitable to us.
    Right now, this class is a temporary version. There are many problems need to solve.
    This class depends MyCommandQueue class, which is very unreasonable, but it also can use now.
    
    """
    def __init__(self, commandQueue=None, group=None, name=None, verbose=None):
        """
        @param commendQueue: the MyCommandQueue object.
        @type commandQueue: MyCommandQueue object
        
        @note: other attributes are not used temporarily.
        
        """
        Thread.__init__(self, group=group, name=name, verbose=verbose)
        self.commandQueue = commandQueue
        self.__lock = None
    
    
    def run(self):
        """
        This method is overwritting the Thread's run() method.
        It has a special pattern to process the method need to run whether want to lock.
        Use the apply() method to run the goal method.
        
        """
        count = 0
        while(True):
            count += 1
            command = self.__getCommandFromQueue()
            self.__getDetailFromCommand(command)
            if not command:
                break
            if self.__lock:
                if self.__lock.acquire():
                    self.__target(*self.__args, **self.__kwargs)
                    self.__lock.release()
            else:
                self.__target(*self.__args, **self.__kwargs)
    
    
    def __getDetailFromCommand(self, command):
        """
        Unpack the MyCommand object, 
        and get some attribute that is useful from it
        
        @param command: an object of MyCommand 
        @type command: MyCommand object
        
        """
        if command:
            self.__lock = command.lock
            self.__target = command.methodObject
            self.__args = command.args
            self.__kwargs = command.kwargs

    
    def __getCommandFromQueue(self):
        """
        This method is used to get a command from myComandQueue one by one.
        It's used temproarily before we find a new way to solve the dependency relationship.
        
        """
        command = self.commandQueue.get()
        
        return command
    
    
    

##just test:
#from myCommand import MyCommand
#from threading import Lock
#num = 1
## lock = Lock()
#lock = None
#def test():
#    global num
#    for i in range(10):
#        num += 1
#        print num
#if __name__ == '__main__':
#    command = MyCommand()
#    command.setCommand(methodObject=test, lock=lock, priority=2, args=[], kwargs={})
#    myThread =  MyThread()
#    myThread1 =  MyThread(commandQueue)
#    myThread.start()
#    myThread1.start()

