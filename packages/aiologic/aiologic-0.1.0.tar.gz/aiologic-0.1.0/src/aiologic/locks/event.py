#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2024 Ilya Egorov <0x42005e1f@gmail.com>
# SPDX-License-Identifier: ISC

__all__ = (
    'Event',
)

from collections import deque

from aiologic.lowlevel import TaskEvent, ThreadEvent, checkpoint


class Event:
    __slots__ = (
        '__is_unset',
        'waiters',
    )
    
    @staticmethod
    def __new__(cls, /, is_set=False):
        self = super(Event, cls).__new__(cls)
        
        self.__is_unset = not is_set
        
        self.waiters = deque()
        
        return self
    
    def __getnewargs__(self, /):
        if self.__is_unset:
            args = ()
        else:
            args = (True,)
        
        return args
    
    def __repr__(self, /):
        return f"Event(is_set={not self.__is_unset})"
    
    def __bool__(self, /):
        return not self.__is_unset
    
    def __await__(self, /):
        rescheduled = False
        
        if self.__is_unset:
            self.waiters.append(event := TaskEvent())
            
            if self.__is_unset:
                success = False
                
                try:
                    success = yield from event.__await__()
                finally:
                    if not success:
                        try:
                            self.waiters.remove(event)
                        except ValueError:
                            pass
                
                rescheduled = True
            else:
                success = True
        else:
            success = True
        
        if not self.__is_unset:
            self.__wakeup()
        
        if not rescheduled:
            yield from checkpoint().__await__()
        
        return success
    
    def wait(self, /, timeout=None):
        if self.__is_unset:
            self.waiters.append(event := ThreadEvent())
            
            if self.__is_unset:
                success = False
                
                try:
                    success = event.wait(timeout)
                finally:
                    if not success:
                        try:
                            self.waiters.remove(event)
                        except ValueError:
                            pass
            else:
                success = True
        else:
            success = True
        
        if not self.__is_unset:
            self.__wakeup()
        
        return success
    
    def set(self, /):
        self.__is_unset = False
        self.__wakeup()
    
    def is_set(self, /):
        return not self.__is_unset
    
    def __wakeup(self, /):
        waiters = self.waiters
        
        while waiters:
            try:
                event = waiters.popleft()
            except IndexError:
                pass
            else:
                event.set()
