#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2024 Ilya Egorov <0x42005e1f@gmail.com>
# SPDX-License-Identifier: ISC

__all__ = (
    'Condition',
)

import sys
import time

from aiologic.lowlevel import shield

from .lot import ParkingLot
from .lock import RLock


class Condition:
    __slots__ = (
        'lot',
        'lock',
    )
    
    @staticmethod
    def __new__(cls, /, lock=None):
        if lock is None:
            lock = RLock()
        
        self = super(Condition, cls).__new__(cls)
        
        self.lot = ParkingLot()
        
        self.lock = lock
        
        return self
    
    def __getnewargs__(self, /):
        return (self.lock,)
    
    def __repr__(self, /):
        return f"Condition({self.lock!r})"
    
    def __bool__(self, /):
        return bool(self.lock)
    
    async def __aenter__(self, /):
        return await self.lock.__aenter__()
    
    async def __aexit__(self, /, exc_type, exc_value, traceback):
        return await self.lock.__aexit__(exc_type, exc_value, traceback)
    
    def __enter__(self, /):
        return self.lock.__enter__()
    
    def __exit__(self, /, exc_type, exc_value, traceback):
        return self.lock.__exit__(exc_type, exc_value, traceback)
    
    def __await__(self, /):
        lot = self.lot
        lock = self.lock
        
        token = lot.park()
        event = yield from token.__aenter__().__await__()
        
        try:
            if isinstance(lock, RLock):
                state = lock._release_save_as_task()
            else:
                yield from lock.__aexit__(None, None, None).__await__()
            
            try:
                success = yield from event.__await__()
            finally:
                if isinstance(lock, RLock):
                    yield from shield(
                        lock._acquire_restore_as_task(state),
                    ).__await__()
                else:
                    yield from shield(
                        lock.__aenter__(),
                    ).__await__()
        finally:
            yield from token.__aexit__(*sys.exc_info()).__await__()
        
        if not success and event.is_set():
            lot.unpark()
        
        return success
    
    def wait(self, /, timeout=None):
        lot = self.lot
        lock = self.lock
        
        with lot.park() as event:
            if isinstance(lock, RLock):
                state = lock._release_save_as_thread()
            else:
                lock.__exit__(None, None, None)
            
            try:
                success = event.wait(timeout)
            finally:
                if isinstance(lock, RLock):
                    lock._acquire_restore_as_thread(state)
                else:
                    lock.__enter__()
        
        if not success and event.is_set():
            lot.unpark()
        
        return success
    
    def wait_for(self, /, predicate, timeout=None):
        success = False
        deadline = None
        
        while not predicate():
            if timeout is not None:
                if deadline is None:
                    deadline = time.monotonic() + timeout
                else:
                    timeout = deadline - time.monotonic()
                    
                    if timeout <= 0:
                        break
            
            self.wait(timeout)
        else:
            success = True
        
        return success
    
    def notify(self, /, count=1):
        return self.lot.unpark(count)
    
    def notify_all(self, /):
        return self.lot.unpark_all()
