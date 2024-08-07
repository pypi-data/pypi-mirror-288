#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2024 Ilya Egorov <0x42005e1f@gmail.com>
# SPDX-License-Identifier: ISC

__all__ = (
    'Empty',
    'SimpleQueue',
)

from collections import deque

from .locks import ParkingLot
from .lowlevel import MISSING

try:
    from queue import Empty
except ImportError:
    class Empty(Exception):
        pass


class SimpleQueue:
    __slots__ = (
        '__lot',
        '__queue'
    )
    
    @staticmethod
    def __new__(cls, /, items=MISSING):
        self = super(SimpleQueue, cls).__new__(cls)
        
        self.__lot = ParkingLot()
        
        if items is MISSING:
            self.__queue = deque()
        else:
            self.__queue = queue = deque(items)
            
            if queue:
                self.__lot.unpark(len(queue), exact=True)
        
        return self
    
    def __getnewargs__(self, /):
        return (list(self.__queue),)
    
    def __repr__(self, /):
        return f"SimpleQueue({list(self.__queue)!r})"
    
    def __bool__(self, /):
        return bool(self.__queue)
    
    def __len__(self, /):
        return len(self.__queue)
    
    async def aput(self, /, item):
        self.__queue.append(item)
        self.__lot.unpark(exact=True)
    
    def put(self, /, item, *, blocking=True, timeout=None):
        self.__queue.append(item)
        self.__lot.unpark(exact=True)
    
    async def aget(self, /):
        await self.__lot.park_as_task(exact=True)
        
        return self.__queue.popleft()
    
    def get(self, /, *, blocking=True, timeout=None):
        success = self.__lot.park_as_thread(
            blocking=blocking,
            timeout=timeout,
            exact=True,
        )
        
        if not success:
            raise Empty
        
        return self.__queue.popleft()
