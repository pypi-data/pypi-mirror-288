#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2024 Ilya Egorov <0x42005e1f@gmail.com>
# SPDX-License-Identifier: ISC

__all__ = (
    'ParkingLot',
)

from weakref import ref
from itertools import repeat
from collections import deque

from aiologic.lowlevel import Flag, TaskEvent, ThreadEvent, checkpoint


class ParkingToken:
    __slots__ = (
        '__weakref__',
        'lot',
        'done',
        'event',
    )
    
    @staticmethod
    def __new__(cls, /, lot):
        self = super(ParkingToken, cls).__new__(cls)
        
        self.lot = lot
        
        self.done = Flag()
        
        return self
    
    @classmethod
    def __init_subclass__(cls, /, **kwargs):
        raise TypeError("type 'ParkingToken' is not an acceptable base type")
    
    def __reduce__(self, /):
        raise TypeError(f"cannot reduce {self!r}")
    
    async def __aenter__(self, /):
        self.event = event = TaskEvent()
        
        self.lot.waiters.append(ref(self))
        self.lot.unpark(0)
        
        return event
    
    async def __aexit__(self, /, exc_type, exc_value, traceback):
        if self.done.set(None):
            try:
                self.lot.waiters.remove(ref(self))
            except ValueError:
                pass
        elif exc_value is not None:
            self.lot.unpark(exact=self.done.get())
        else:
            self.event.set()
    
    def __enter__(self, /):
        self.event = event = ThreadEvent()
        
        self.lot.waiters.append(ref(self))
        self.lot.unpark(0)
        
        return event
    
    def __exit__(self, /, exc_type, exc_value, traceback):
        if self.done.set(None):
            try:
                self.lot.waiters.remove(ref(self))
            except ValueError:
                pass
        elif exc_value is not None:
            self.lot.unpark(exact=self.done.get())
        else:
            self.event.set()


class ParkingLot:
    __slots__ = (
        'waiters', 'pending',
    )
    
    @staticmethod
    def __new__(cls, /):
        self = super(ParkingLot, cls).__new__(cls)
        
        self.waiters = deque()
        self.pending = []
        
        return self
    
    def __repr__(self, /):
        return 'ParkingLot()'
    
    def park(self, /):
        return ParkingToken(self)
    
    async def park_as_task(self, /, *, exact=None):
        if pending := self.pending:
            try:
                success = pending.pop()
            except IndexError:
                success = False
        else:
            success = False
        
        if not success:
            if exact is None:
                token = ParkingToken(self)
                
                async with token as event:
                    success = await event
                
                if not success and event.is_set():
                    self.unpark(exact=token.done.get())
            else:
                token = (event := TaskEvent(), is_unset := [True])
                
                self.waiters.append(token)
                self.unpark(0)
                
                try:
                    success = await event
                finally:
                    if not success:
                        if is_unset:
                            try:
                                is_unset.pop()
                            except IndexError:
                                self.unpark(exact=exact)
                            else:
                                try:
                                    self.waiters.remove(token)
                                except ValueError:
                                    pass
                        else:
                            self.unpark(exact=exact)
        else:
            await checkpoint()
        
        return success
    
    def park_as_thread(self, /, *, blocking=True, timeout=None, exact=None):
        if pending := self.pending:
            try:
                success = pending.pop()
            except IndexError:
                success = False
        else:
            success = False
        
        if not success and blocking:
            if exact is None:
                token = ParkingToken(self)
                
                with token as event:
                    success = event.wait(timeout)
                
                if not success and event.is_set():
                    self.unpark(exact=token.done.get())
            else:
                token = (event := ThreadEvent(), is_unset := [True])
                
                self.waiters.append(token)
                self.unpark(0)
                
                try:
                    success = event.wait(timeout)
                finally:
                    if not success:
                        if is_unset:
                            try:
                                is_unset.pop()
                            except IndexError:
                                self.unpark(exact=exact)
                            else:
                                try:
                                    self.waiters.remove(token)
                                except ValueError:
                                    pass
                        else:
                            self.unpark(exact=exact)
        
        return success
    
    def park_nowait(self, /):
        if pending := self.pending:
            try:
                success = pending.pop()
            except IndexError:
                success = False
        else:
            success = False
        
        return success
    
    def unpark(self, /, count=1, *, exact=False):
        waiters = self.waiters
        pending = self.pending
        
        if exact and count != 0:
            if count == 1:
                self.pending.append(True)
            else:
                self.pending.extend(repeat(True, count))
            
            unparked = count
        else:
            unparked = 0
        
        while waiters:
            if pending:
                try:
                    is_pending = pending.pop()
                except IndexError:
                    is_pending = False
            else:
                is_pending = False
            
            if not is_pending and unparked == count:
                break
            
            try:
                maybe_token = waiters.popleft()
            except IndexError:
                pass
            else:
                if callable(maybe_token):
                    if (token := maybe_token()) is not None:
                        if token.done.set(is_pending or exact):
                            token.event.set()
                            
                            if not is_pending:
                                unparked += 1
                            
                            is_pending = False
                else:
                    event, is_unset = maybe_token
                    
                    if is_unset:
                        try:
                            is_unset.pop()
                        except IndexError:
                            pass
                        else:
                            event.set()
                            
                            if not is_pending:
                                unparked += 1
                            
                            is_pending = False
            
            if is_pending:
                pending.append(True)
        
        return unparked
    
    def unpark_all(self, /):
        waiters = self.waiters
        pending = self.pending
        
        unparked = 0
        
        while waiters:
            if pending:
                try:
                    is_pending = pending.pop()
                except IndexError:
                    is_pending = False
            else:
                is_pending = False
            
            try:
                maybe_token = waiters.popleft()
            except IndexError:
                pass
            else:
                if callable(maybe_token):
                    if (token := maybe_token()) is not None:
                        if token.done.set(is_pending):
                            token.event.set()
                            
                            if not is_pending:
                                unparked += 1
                            
                            is_pending = False
                else:
                    event, is_unset = maybe_token
                    
                    if is_unset:
                        try:
                            is_unset.pop()
                        except IndexError:
                            pass
                        else:
                            event.set()
                            
                            if not is_pending:
                                unparked += 1
                            
                            is_pending = False
            
            if is_pending:
                pending.append(True)
        
        return unparked
