#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2024 Ilya Egorov <0x42005e1f@gmail.com>
# SPDX-License-Identifier: ISC

__all__ = (
    'Semaphore', 'BoundedSemaphore',
)

from .lot import ParkingLot


class Semaphore:
    __slots__ = (
        'lot',
        'initial_value',
    )
    
    @staticmethod
    def __new__(cls, /, initial_value=1):
        self = super(Semaphore, cls).__new__(cls)
        
        self.lot = ParkingLot()
        self.lot.unpark(initial_value, exact=True)
        
        self.initial_value = initial_value
        
        return self
    
    def __getnewargs__(self, /):
        if (initial_value := self.initial_value) != 1:
            args = (initial_value,)
        else:
            args = ()
        
        return args
    
    def __repr__(self, /):
        return f"Semaphore({self.initial_value!r})"
    
    async def __aenter__(self, /):
        await self.acquire_as_task()
        
        return self
    
    async def __aexit__(self, /, exc_type, exc_value, traceback):
        self.release_as_task()
    
    def __enter__(self, /):
        self.acquire_as_thread()
        
        return self
    
    def __exit__(self, /, exc_type, exc_value, traceback):
        self.release_as_thread()
    
    async def acquire_as_task(self, /):
        return await self.lot.park_as_task(exact=True)
    
    def acquire_as_thread(self, /, *, blocking=True, timeout=None):
        return self.lot.park_as_thread(
            blocking=blocking,
            timeout=timeout,
            exact=True,
        )
    
    def release_as_task(self, /, count=1):
        self.lot.unpark(count, exact=True)
    
    def release_as_thread(self, /, count=1):
        self.lot.unpark(count, exact=True)
    
    @property
    def value(self, /):
        return len(self.lot.pending)


class BoundedSemaphore:
    __slots__ = (
        'lot',
        'locked',
        'initial_value', 'max_value',
    )
    
    @staticmethod
    def __new__(cls, /, initial_value=None, max_value=None):
        if initial_value is None:
            if max_value is None:
                initial_value = max_value = 1
            else:
                initial_value = max_value
        elif max_value is None:
            max_value = initial_value
        
        self = super(BoundedSemaphore, cls).__new__(cls)
        
        self.lot = ParkingLot()
        self.lot.unpark(initial_value, exact=True)
        
        self.locked = [True] * (max_value - initial_value)
        
        self.initial_value = initial_value
        self.max_value = max_value
        
        return self
    
    def __getnewargs__(self, /):
        initial_value = self.initial_value
        max_value = self.max_value
        
        if initial_value != max_value:
            args = (initial_value, max_value)
        elif initial_value != 1:
            args = (initial_value,)
        else:
            args = ()
        
        return args
    
    def __repr__(self, /):
        initial_value = self.initial_value
        max_value = self.max_value
        
        if initial_value != max_value:
            args_repr = f"{initial_value!r}, max_value={max_value!r}"
        else:
            args_repr = f"{initial_value!r}"
        
        return f"BoundedSemaphore({args_repr})"
    
    def __bool__(self, /):
        return len(self.lot.pending) != self.max_value
    
    async def __aenter__(self, /):
        await self.acquire_as_task()
        
        return self
    
    async def __aexit__(self, /, exc_type, exc_value, traceback):
        self.release_as_task()
    
    def __enter__(self, /):
        self.acquire_as_thread()
        
        return self
    
    def __exit__(self, /, exc_type, exc_value, traceback):
        self.release_as_thread()
    
    async def acquire_as_task(self, /):
        success = await self.lot.park_as_task(exact=True)
        
        if success:
            self.locked.append(True)
        
        return success
    
    def acquire_as_thread(self, /, *, blocking=True, timeout=None):
        success = self.lot.park_as_thread(
            blocking=blocking,
            timeout=timeout,
            exact=True,
        )
        
        if success:
            self.locked.append(True)
        
        return success
    
    def release_as_task(self, /):
        try:
            self.locked.pop()
        except IndexError:
            raise RuntimeError('semaphore released too many times') from None
        
        self.lot.unpark(exact=True)
    
    def release_as_thread(self, /):
        try:
            self.locked.pop()
        except IndexError:
            raise RuntimeError('semaphore released too many times') from None
        
        self.lot.unpark(exact=True)
    
    @property
    def value(self, /):
        return len(self.lot.pending)
