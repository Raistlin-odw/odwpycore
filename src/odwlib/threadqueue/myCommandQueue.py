"""
Created on 2013-5-1
 
@author: lavenda
"""
#!/usr/bin/env python2.6
# -*- coding:utf-8 -*-
from Queue import Queue
import heapq
import time

class MyCommandQueue(Queue):
    """
    This class will make a queue of the commands submited.
    Also, it provides two method to control the queue, such as put(command) and get().
    It use the heapq module and inherit the Queue class,
    and overwrite some methods in Queue class for add the element called priority.
    Now it can add any different priority commands to the queue 
    so that it can be added diferent priority commands dynamically.
    
    reference: https://github.com/hongloull/python/blob/master/src/core/threading/priorityQueue.py
    """
    
    def __init__(self, maxsize):
        """
        @param maxsize: means the max length of queue
        @type maxsize: int type
        
        """
        Queue.__init__(self, maxsize)
        self.maxsize = maxsize
        self.queue = []
    
    
    def _put(self, item):
        """ 
        Put a new item in the queue. Overwrite the _put method in the Queue class.
        
        @param item: it is a node of a binary tree
        @type item: tuple type
        
        @return: None type
        
        """
        return heapq.heappush(self.queue, item)
    
    
    def _get(self):
        """
        Get a new item in the queue.Overwrite the _get method in the Queue class.
        
        @return: a tuple type, it is a node of a binary tree.
        
        """
        
        return heapq.heappop(self.queue)
    
    
    def put(self, command, block=True, timeout=None):
        """
        This method is used to put a MyCommand object to the queue.
        
        @param command: an object of class MyCommand.
        @type command: MyCommand object
        
        @return: a boolean type, means whether putting a object into queue is success.
        
        @note: other attributes are not useful temporarily
        
        """
        priority = command.priority
        item = (priority, command)
        decorated_item = priority, time.time(), item
        Queue.put(self, decorated_item, block, timeout)
    
    
    def get(self, block=True, timeout=None):
        """
        This method is used to get a MyCommand object from the queue.
        
        @return: a MyCommand object or None. If queue is not empty, 
                it will return an object, otherwise return None
        
        @note: all the attributes are not useful temporarily
        
        """
        
        if self.queue:
            item = Queue.get(self, block, timeout)[2]
            command = item[1]
            return command
        else:
            return None




def main():
    from myCommand import MyCommand
    myCommandQueue = MyCommandQueue(100)
    command = MyCommand()
    command.setCommand(methodObject=object, lock=object,
                       priority=2, args=[], kwargs={})
    myCommandQueue.put(command)
    print myCommandQueue.queue
    command1 = myCommandQueue.get()
    command2 = myCommandQueue.get()
    print command1, command2


if __name__ == '__main__':
    main()
